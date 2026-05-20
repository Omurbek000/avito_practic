from .models import *
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'phone_number','age')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        user = User(email=email, username=username, **validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({"email": "Пользователь с таким email не найден"})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Неверный пароль"})



        self.context['user'] = user
        return data

    def to_representation(self, instance):
        user = self.context['user']
        refresh = RefreshToken.for_user(user)

        return {
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get('refresh')
        try:
            RefreshToken(token)
        except Exception:
            raise serializers.ValidationError({"refresh": "Невалидный токен"})
        return attrs




class UserSerializers(serializers.ModelSerializer):
    get_user_rating = serializers.SerializerMethodField()
    get_user_people = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'age', 'phone_number', 'avatar','get_user_rating', 'get_user_people']
        
    def get_user_rating(self, obj):
        return obj.get_user_rating()
    
    def get_user_people(self, obj):
        return obj.get_user_people()


class OwnerShortSerializer(serializers.ModelSerializer):
    """Минимальная информация о продавце для списка товаров."""
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar']


class OwnerDetailSerializer(serializers.ModelSerializer):
    """Расширенная информация о продавце для детальной страницы товара."""
    get_user_rating = serializers.SerializerMethodField()
    get_user_people = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'get_user_rating', 'get_user_people']

    def get_user_rating(self, obj):
        return obj.get_user_rating()

    def get_user_people(self, obj):
        return obj.get_user_people()



class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cartegory
        fields = ['category_name', 'category_image']


class SubCategorySimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['sub_category_name']  


class CategoryDetailSerializers(serializers.ModelSerializer):
    sub_category = SubCategorySimpleSerializers(read_only=True, many=True)
    class Meta:
        model = Cartegory
        fields = ['id', 'category_name', 'category_image', 'sub_category']


class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product', 'product_image']


class ProductListSerializers(serializers.ModelSerializer):
    product_image = ProductImageSerializers(source='images', read_only=True, many=True)  
    owner = OwnerShortSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'description', 'product_image','owner']


class ProductDetailSerializers(serializers.ModelSerializer):
    product_image = ProductImageSerializers(source='images', read_only=True, many=True)  
    owner = OwnerDetailSerializer(read_only=True)   
    created_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    get_avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'article_number', 'product_name', 'price', 'description', 'product_type', 'created_date', 'product_image','get_avg_rating','get_count_people','owner']
        
    def get_avg_rating(self, obj):
        return obj.get_avg_rating()
    
    def get_count_people(self, obj):
        return obj.get_count_people()


class SubCategoryListSerializers(serializers.ModelSerializer):
    category = CategoryListSerializers(source='category_name', read_only=True)  
    class Meta:
        model = SubCategory
        fields = ['id', 'category', 'sub_category_name', 'sub_category_image']


class SubCategoryDetailSerializers(serializers.ModelSerializer):
    sub_category_product = ProductListSerializers(read_only=True, many=True)
    class Meta:
        model = SubCategory
        fields = ['sub_category_name', 'sub_category_product']


class ReviewSerializers(serializers.ModelSerializer):
    product_review = ProductListSerializers(source='product', read_only=True)
    user_review = UserSerializers(source='user', read_only=True)
    created_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    class Meta:
        model = Review
        fields = ['product_review', 'user_review', 'product', 'user', 'stars', 'comment', 'created_date']
        
        
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializers(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True,source='product')
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id','product','product','product_id','quantity','total_price']
        
    def get_total_price(self, obj):
        return obj.total_price()
    

class CartSerializer(serializers.ModelSerializer):
    cart_item = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id','cart_item','user','total_price']
        
    def get_total_price(self, obj):
        return obj.total_price()


class FavoriteItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializers(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, sourse='product')
    
    class Meta:
        model = FavoriteItem
        fields = ['product','product_id','favorite']    



class FavoriteSerializer(serializers.ModelSerializer):
    favorite_item = FavoriteItemSerializer(read_only=True, many=True)
    class Meta:
        model = Favorite
        fields = ['id','user','favorite_item']