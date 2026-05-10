from .models import User, Cartegory, SubCategory, Product, Review, ProductImage
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','age','phone_number','avatar']


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Cartegory
        fields = ['id','category_name','category_image']

class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cartegory
        fields = ['category_name','category_image']


class SubCategorySerializers(serializers.ModelSerializer):
    category = CategoryListSerializers()
    class Meta:
        model =  SubCategory
        fields = ['category','sub_category_name','sub_category_image']


class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product','product_image']


class ProductListSerializers(serializers.ModelSerializer):
    product_image = ProductImageSerializers(read_only=True, many=True)
    class Meta:
        model = Product
        fields = ['product_name','price','description','product_image']

class ProductDetailSerializers(serializers.ModelSerializer):
    product_image = ProductImageSerializers(read_only=True)
    class Meta:
        model = Product
        fields = ['id','article_number','product_name','price','description','product_type','created_date','product_image']



class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'