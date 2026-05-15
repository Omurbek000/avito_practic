from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    CategoryListViewSet, CategoryDetailAPIView,
    SubCategoryListAPIView, SubCategoryDetailAPIView,
    ProductListAPIView, ProductDetailAPIView,
    ProductImageViewSet,
    ReviewViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryListViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('subcategories/', SubCategoryListAPIView.as_view()),
    path('subcategories/<int:pk>/', SubCategoryDetailAPIView.as_view()),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view()),
    path('products/', ProductListAPIView.as_view()),
    path('products/<int:pk>/', ProductDetailAPIView.as_view()),
] + router.urls