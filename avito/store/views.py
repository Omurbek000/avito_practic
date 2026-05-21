from .serializers import *
from .models import *
from rest_framework import viewsets, generics, permissions, status, serializers
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from .pagination import ProductPagination

from .permissions import IsProductOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomLoginView(generics.GenericAPIView):
    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'detail': 'Невалидный токен'}, status=status.HTTP_400_BAD_REQUEST)



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
    
    
    
class CartAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def retrieve(self, request,**args, **kwargs)
    cart, created = Cart.objects.get_or_created(user=self.request.user)
    serializer = self.get_serializer(cart)
    return Response(serializer.data)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    
    
    def get_queryset(self):
        return  CartItem.filter(cart__user=self.request.user)
    
    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
       
    

class FavoriteAPIView(generics.RetrieveAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        favorite, created = Favorite.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(favorite)
        return Response(serializer.data)
    


class FavoriteItemViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return FavoriteItem.objects.filter(favorite__user=self.request.user)
    
    def perform_create(self, serializer):
        favorite , created = Favorite.objects.get_or_create(user=self.request.user)
        product = serializer.validate_data['product']
        
        if FavoriteItem.objects.filter(favorite=favorite, product=product).exists():
            raise serializers.ValidationError('Товар уже есть в избранной ')
        
        serializer.save(favorite=favorite)