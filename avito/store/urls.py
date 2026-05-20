from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

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
    path('register/',RegisterView.as_view(),name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(),name='logaut'),
    path('cart/', CartAPIView.as_view(), name='cart_detail'),
    path('cart_item/', CartItemViewSet.as_view({'get':'list','post': 'create'})),
    path('cart_item/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    
    path('products/<int:pk>/<str:action>/', ChangeProductStatusAPIView.as_view(), name='product-change-status'),
] + router.urls