from .models import User, Cartegory, SubCategory, Product, Review, ProductImage
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'age', 'phone_number', 'avatar']


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
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'description', 'product_image']


class ProductDetailSerializers(serializers.ModelSerializer):
    product_image = ProductImageSerializers(source='images', read_only=True, many=True)  
    created_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    class Meta:
        model = Product
        fields = ['id', 'article_number', 'product_name', 'price', 'description', 'product_type', 'created_date', 'product_image']


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