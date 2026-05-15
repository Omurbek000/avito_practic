from django_filters import FilterSet
from .models import Product

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'product_type': ['exact'],
            'sub_category': ['exact'],
            'product_name': ['exact'],
            'price': ['gt','lt']
            
        }