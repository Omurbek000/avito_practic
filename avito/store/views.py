from .serializers import UserSerializers, CategorySerializers, SubCategorySerializers, ProductImageSerializers, ProductSerializers, ReviewSerializers
from . models import User, Cartegory, SubCategory, Product, ProductImage, Review
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Cartegory.objects.all()
    serializer_class = CategorySerializers


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializers


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
