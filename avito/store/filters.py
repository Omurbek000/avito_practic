from django_filters import FilterSet
from .models import Product


class ProductFilter(FilterSet):
    """
    Фильтры для списка товаров.

    Доступные параметры в запросе:
    - product_type=new         — фильтр по состоянию товара (new/used/reserved/sold)
    - sub_category=1           — фильтр по подкатегории (ID)
    - product_name=iPhone      — точное совпадение по названию
    - price__gt=1000           — цена больше чем
    - price__lt=50000          — цена меньше чем

    Пример: /products/?price__gt=1000&price__lt=50000&product_type=new
    """

    class Meta:
        model = Product
        fields = {
            "product_type": ["exact"],
            "sub_category": ["exact"],
            "product_name": ["exact"],
            "price": ["gt", "lt"],
        }
