from .models import User, Cartegory, SubCategory, Product, Review, ProductImage
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'status', 'age','username']


class UserDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['last_name', 'user_name', 'first_name','avatar']


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Cartegory
        fields = '__all__'


class SubCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model =  SubCategory
        fields = '__all__'


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'