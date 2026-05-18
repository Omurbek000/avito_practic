from .serializers import *
from .models import User, Cartegory, SubCategory, Product, ProductImage, Review
from rest_framework import viewsets, generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from .pagination import ProductPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class CategoryListViewSet(viewsets.ModelViewSet):
    queryset = Cartegory.objects.all()
    serializer_class = CategoryListSerializers


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Cartegory.objects.all()
    serializer_class = CategoryDetailSerializers


class SubCategoryListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryListSerializers


class SubCategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryDetailSerializers


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    ordering_fields = ['price', 'created_date', 'product_type']
    pagination_class = ProductPagination  


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializers


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializers


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]