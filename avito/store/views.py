from .serializers import *
from .models import User, Cartegory, SubCategory, Product, ProductImage, Review
from rest_framework import viewsets, generics, permissions, status
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


class ChangeProductStatusAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsProductOwner]

    def post(self, request, pk, action):
        product = get_object_or_404(Product, pk=pk)
        
        # Явно запускаем проверку object-level permissions
        self.check_object_permissions(request, product)

        allowed_transitions = {
            'reserve': ['new', 'used'],
            'sell': ['new', 'used', 'reserved'],
        }
        if action not in allowed_transitions:
            return Response(
                {"error": "Недопустимое действие. Используйте 'reserve' или 'sell'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if product.product_type not in allowed_transitions[action]:
            return Response(
                {"error": f"Нельзя перевести товар из статуса '{product.product_type}' в '{action}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_status = 'reserved' if action == 'reserve' else 'sold'
        product.product_type = new_status
        product.save()
        return Response({"status": new_status}, status=status.HTTP_200_OK)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializers


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]