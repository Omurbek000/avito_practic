from . views import UserViewSet, CategoryViewSet, SubCategoryViewSet, ProductViewSet, ProductImageViewSet, ReviewViewSet
from django.urls import path, include

urlpatterns = [
    path('user/', UserViewSet.as_view(), name='users'),
    path('category/', CategoryViewSet.as_view(), name='categorys'),
    path('sub_category/', SubCategoryViewSet.as_view(), name='sub_categorys'),
    path('product/', ProductViewSet.as_view(), name='products'),
    path('product_image/', ProductImageViewSet.as_view(), name='product_images'),
    path('review/', ReviewViewSet.as_view(), name='reviews'),
    
]
