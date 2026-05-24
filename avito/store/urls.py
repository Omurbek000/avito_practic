from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView, CustomLoginView, LogoutView,
    UserViewSet,
    CategoryListViewSet, CategoryDetailAPIView,
    SubCategoryListAPIView, SubCategoryDetailAPIView,
     ProductDetailAPIView, ProductImageViewSet,
    ReviewViewSet,
    CartAPIView, CartItemViewSet,
    FavoriteAPIView, FavoriteItemViewSet, ProductListCreateAPIView,
)




router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"categories", CategoryListViewSet, basename="category")
router.register(r"product-images", ProductImageViewSet, basename="product-image")
router.register(r"reviews", ReviewViewSet, basename="review")


# URL маршруты

urlpatterns = [

    # Авторизация
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # Категории
    path("categories/<int:pk>/", CategoryDetailAPIView.as_view(), name="category-detail"),

    # Подкатегории
    path("subcategories/", SubCategoryListAPIView.as_view(), name="subcategory-list"),
    path("subcategories/<int:pk>/", SubCategoryDetailAPIView.as_view(), name="subcategory-detail"),

    # Товары
    # path("products/", ProductListAPIView.as_view(), name="product-list"),
    path('products/', ProductListCreateAPIView.as_view()),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),

    # Корзина
    path("cart/", CartAPIView.as_view(), name="cart-detail"),
    path("cart_item/", CartItemViewSet.as_view({"get": "list", "post": "create"}), name="cart-item-list"),
    path("cart_item/<int:pk>/", CartItemViewSet.as_view({"put": "update", "patch": "partial_update", "delete": "destroy"}), name="cart-item-detail"),

    # избранное
    path("favorite/", FavoriteAPIView.as_view(), name="favorite-detail"),
    path("favorite_item/", FavoriteItemViewSet.as_view({"get": "list", "post": "create"}), name="favorite-item-list"),
    path("favorite_item/<int:pk>/", FavoriteItemViewSet.as_view({"delete": "destroy"}), name="favorite-item-detail"),

] + router.urls
