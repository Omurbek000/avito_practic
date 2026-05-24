from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    User, Category, SubCategory,
    Product, ProductImage, Review,
    Cart, CartItem, Favorite, FavoriteItem,
)



# Авторизация


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя.
    Поле password скрыто из ответа (write_only).
    """

    class Meta:
        model = User
        fields = ("email", "username", "password", "phone_number", "age")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        """Проверяем что email ещё не занят."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует"
            )
        return value

    def create(self, validated_data):
        """
        Создаём пользователя через set_password
        чтобы пароль сохранялся в хэшированном виде, а не открытом тексте.
        """
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomLoginSerializer(serializers.Serializer):
    """
    Сериализатор для входа по email и паролю.
    Возвращает JWT токены (access + refresh).
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "Пользователь с таким email не найден"}
            )

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Неверный пароль"})

        # Сохраняем пользователя в контексте для to_representation
        self.context["user"] = user
        return data

    def to_representation(self, instance):
        """Формируем ответ с токенами после успешной авторизации."""
        user = self.context["user"]
        refresh = RefreshToken.for_user(user)

        return {
            "user": {
                "username": user.username,
                "email": user.email,
            },
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    """
    Сериализатор для выхода.
    Принимает refresh токен и добавляет его в чёрный список (blacklist).
    """

    refresh = serializers.CharField()

    def validate(self, attrs):
        """Проверяем что токен валидный перед добавлением в blacklist."""
        token = attrs.get("refresh")
        try:
            RefreshToken(token)
        except Exception:
            raise serializers.ValidationError({"refresh": "Невалидный токен"})
        return attrs


# Пользователь


class UserSerializers(serializers.ModelSerializer):
    """
    Публичный профиль пользователя.
    Включает рейтинг и количество отзывов.
    """

    get_user_rating = serializers.SerializerMethodField()
    get_user_people = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "age",
            "phone_number", "avatar",
            "get_user_rating", "get_user_people",
        ]

    def get_user_rating(self, obj):
        """Средний рейтинг пользователя."""
        return obj.get_user_rating()

    def get_user_people(self, obj):
        """Количество отзывов о пользователе."""
        return obj.get_user_people()


# Владелец товара (owner)
# Два варианта: краткий для списка и детальный для страницы товара


class OwnerShortSerializer(serializers.ModelSerializer):
    """
    Краткая информация о владельце для отображения в списке товаров.
    Показываем только имя и аватар — не перегружаем ответ.
    """

    class Meta:
        model = User
        fields = ["id", "username", "avatar"]


class OwnerDetailSerializer(serializers.ModelSerializer):
    """
    Детальная информация о владельце для страницы конкретного товара.
    Показываем рейтинг и контактные данные.
    """

    get_user_rating = serializers.SerializerMethodField()
    get_user_people = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "avatar",
            "phone_number", "get_user_rating", "get_user_people",
        ]

    def get_user_rating(self, obj):
        return obj.get_user_rating()

    def get_user_people(self, obj):
        return obj.get_user_people()



# Категории


class CategoryListSerializers(serializers.ModelSerializer):
    """Краткий список категорий (название + картинка)."""

    class Meta:
        model = Category
        fields = ["id", "category_name", "category_image"]


class SubCategorySimpleSerializers(serializers.ModelSerializer):
    """Минимальная информация о подкатегории — используется внутри CategoryDetail."""

    class Meta:
        model = SubCategory
        fields = ["id", "sub_category_name"]


class CategoryDetailSerializers(serializers.ModelSerializer):
    """
    Детальная страница категории.
    Включает список всех подкатегорий.
    """

    sub_category = SubCategorySimpleSerializers(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ["id", "category_name", "category_image", "sub_category"]


class SubCategoryListSerializers(serializers.ModelSerializer):
    """Список подкатегорий с родительской категорией."""

    category = CategoryListSerializers(source="category_name", read_only=True)

    class Meta:
        model = SubCategory
        fields = ["id", "category", "sub_category_name", "sub_category_image"]


class SubCategoryDetailSerializers(serializers.ModelSerializer):
    """
    Детальная страница подкатегории.
    Включает все товары в этой подкатегории.
    """

    sub_category_product = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ["id", "sub_category_name", "sub_category_product"]

    def get_sub_category_product(self, obj):
        # Используем краткий сериализатор товара (определён ниже)
        products = obj.sub_category_product.all()
        return ProductListSerializers(products, many=True, context=self.context).data



# Товары


class ProductImageSerializers(serializers.ModelSerializer):
    """Сериализатор для изображений товара."""

    class Meta:
        model = ProductImage
        fields = ["id", "product", "product_image"]


class ProductListSerializers(serializers.ModelSerializer):
    """
    Краткая карточка товара для списков и каталога.
    Включает фото и краткую информацию о владельце.
    """

    product_image = ProductImageSerializers(source="images", read_only=True, many=True)
    owner = OwnerShortSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "product_name", "price",
            "description", "product_image", "owner",
        ]


class ProductDetailSerializers(serializers.ModelSerializer):
    """
    Полная информация о товаре для страницы объявления.
    Включает рейтинг, фото и детальную информацию о владельце.
    """

    product_image = ProductImageSerializers(source="images", read_only=True, many=True)
    owner = OwnerDetailSerializer(read_only=True)
    created_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    get_avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "article_number", "product_name", "price",
            "description", "product_type", "created_date",
            "product_image", "get_avg_rating", "get_count_people", "owner",
        ]

    def get_avg_rating(self, obj):
        """Средний рейтинг товара."""
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        """Количество отзывов на товар."""
        return obj.get_count_people()



# Отзывы

class ReviewSerializers(serializers.ModelSerializer):
    """
    Отзыв на товар.
    product и user — ID для записи, вложенные объекты для чтения.
    """

    product_review = ProductListSerializers(source="product", read_only=True)
    user_review = UserSerializers(source="user", read_only=True)
    created_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = Review
        fields = [
            "id", "product_review", "user_review",
            "product", "user", "stars", "comment", "created_date",
        ]



# Корзина


class CartItemSerializer(serializers.ModelSerializer):
    """
    Позиция в корзине.
    - product (read_only) — полная карточка товара для отображения
    - product_id (write_only) — ID товара для добавления в корзину
    - total_price — итоговая сумма позиции (цена × количество)
    """

    product = ProductListSerializers(source="product_cart", read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source="product_cart",  
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        
        fields = ["id", "product", "product_id", "quantity", "total_price"]

    def get_total_price(self, obj):
        """Стоимость позиции = цена × количество."""
        
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    """
    Корзина пользователя со всеми позициями и итоговой суммой.
    """

    cart_item = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "cart_item", "total_price"]

    def get_total_price(self, obj):
        """Общая сумма всех товаров в корзине."""
        
        return obj.get_total_price()



# Избранное


class FavoriteItemSerializer(serializers.ModelSerializer):
    """
    Товар в избранном.
    - product (read_only) — карточка товара для отображения
    - product_id (write_only) — ID товара для добавления в избранное
    """

    product = ProductListSerializers(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source="product",  
    )

    class Meta:
        model = FavoriteItem
        fields = ["id", "product", "product_id", "favorite"]


class FavoriteSerializer(serializers.ModelSerializer):
    """Список избранного пользователя со всеми товарами."""

    favorite_item = FavoriteItemSerializer(read_only=True, many=True)

    class Meta:
        model = Favorite
        fields = ["id", "user", "favorite_item"]


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового товара.
    owner устанавливается автоматически из request.user во view.
    """
    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'price', 'description',
            'product_type', 'sub_category',
        ]