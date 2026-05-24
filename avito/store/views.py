from rest_framework import viewsets, generics, permissions, status, serializers
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from .filters import ProductFilter
from .pagination import ProductPagination
from .permissions import IsProductOwner
from .models import (
    User, Category, SubCategory,
    Product, ProductImage, Review,
    Cart, CartItem, Favorite, FavoriteItem,
)
from .serializers import (
    RegisterSerializer, CustomLoginSerializer, LogoutSerializer,
    UserSerializers,
    CategoryListSerializers, CategoryDetailSerializers,
    SubCategoryListSerializers, SubCategoryDetailSerializers,
    ProductListSerializers, ProductDetailSerializers, ProductImageSerializers,
    ReviewSerializers,
    CartSerializer, CartItemSerializer,
    FavoriteSerializer, FavoriteItemSerializer, ProductCreateSerializer,
)


from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


# Авторизация


class RegisterView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    Доступно всем (permission не указан — по умолчанию AllowAny).
    POST /register/
    """

    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(generics.GenericAPIView):
    """
    Вход по email и паролю.
    Возвращает JWT токены access и refresh.
    POST /login/
    """

    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    """
    Выход — добавляет refresh токен в blacklist.
    После этого токен становится недействительным.
    POST /logout/
    """

    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(
                {"detail": "Невалидный токен"},
                status=status.HTTP_400_BAD_REQUEST,
            )



# Пользователь


class UserViewSet(viewsets.ModelViewSet):
    """
    Профиль пользователя.
    Авторизованный пользователь видит и редактирует только свой профиль.
    GET/PUT/PATCH/DELETE /users/
    """

    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Возвращаем только профиль текущего пользователя
        return User.objects.filter(id=self.request.user.id)



# Категории

class CategoryListViewSet(viewsets.ModelViewSet):
    """
    CRUD для категорий.
    GET /categories/ — список всех категорий
    POST /categories/ — создать категорию (только админ)
    """

    queryset = Category.objects.all()
    serializer_class = CategoryListSerializers
  


class CategoryDetailAPIView(generics.RetrieveAPIView):
    """
    Детальная страница категории со списком подкатегорий.
    GET /categories/<pk>/
    """

    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializers



# Подкатегории


class SubCategoryListAPIView(generics.ListAPIView):
    """
    Список всех подкатегорий.
    GET /subcategories/
    """

    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryListSerializers


class SubCategoryDetailAPIView(generics.RetrieveAPIView):
    """
    Детальная страница подкатегории со списком товаров.
    GET /subcategories/<pk>/
    """

    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryDetailSerializers



# Товары


# class ProductListAPIView(generics.ListAPIView):
#     """
#     Список товаров с фильтрацией, поиском, сортировкой и пагинацией.

#     Параметры:
#     - search=<название> — поиск по названию
#     - ordering=price / -price / created_date — сортировка
#     - Фильтры из ProductFilter (цена, тип, подкатегория и т.д.)

#     GET /products/
#     """

#     queryset = Product.objects.all()
#     serializer_class = ProductListSerializers
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_class = ProductFilter
#     search_fields = ["product_name"]
#     ordering_fields = ["price", "created_date", "product_type"]
#     pagination_class = ProductPagination

class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /products/ — список товаров (доступно всем)
    POST /products/ — создать объявление (только авторизованным)
    """
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    ordering_fields = ['price', 'created_date', 'product_type']
    pagination_class = ProductPagination
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductListSerializers

    def get_permissions(self):
        # GET — все, POST — только авторизованные
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        # Автоматически ставим owner = текущий пользователь
        serializer.save(owner=self.request.user)




class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    Детальная страница товара с рейтингом и информацией о владельце.
    GET /products/<pk>/
    """

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializers


class ProductImageViewSet(viewsets.ModelViewSet):
    """
    CRUD для изображений товара.
    GET/POST/DELETE /product-images/
    """

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializers



# Отзывы


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Отзывы на товары.
    - Читать могут все (IsAuthenticatedOrReadOnly)
    - Создавать/редактировать только авторизованные пользователи
    GET /reviews/ — список отзывов
    POST /reviews/ — оставить отзыв
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



# Корзина


class CartAPIView(generics.RetrieveAPIView):
    """
    Корзина текущего пользователя.
    Если корзины ещё нет — создаётся автоматически.
    GET /cart/
    """

    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    """
    Управление позициями в корзине.
    GET /cart_item/ — список позиций в корзине текущего пользователя
    POST /cart_item/ — добавить товар в корзину
    PUT/DELETE /cart_item/<pk>/ — изменить количество или удалить позицию
    """

    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
       
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        # Получаем или создаём корзину для текущего пользователя
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)



# Избранное


class FavoriteAPIView(generics.RetrieveAPIView):
    """
    Список избранного текущего пользователя.
    Если списка ещё нет — создаётся автоматически.
    GET /favorite/
    """

    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        favorite, created = Favorite.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(favorite)
        return Response(serializer.data)


class FavoriteItemViewSet(viewsets.ModelViewSet):
    """
    Управление товарами в избранном.
    GET /favorite_item/ — список избранных товаров
    POST /favorite_item/ — добавить товар в избранное
    DELETE /favorite_item/<pk>/ — убрать товар из избранного
    """

    serializer_class = FavoriteItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteItem.objects.filter(favorite__user=self.request.user)

    def perform_create(self, serializer):
        favorite, created = Favorite.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data["product"]

        # Проверяем — товар уже есть в избранном?
        if FavoriteItem.objects.filter(favorite=favorite, product=product).exists():
            raise serializers.ValidationError("Товар уже есть в избранном")

        serializer.save(favorite=favorite)
