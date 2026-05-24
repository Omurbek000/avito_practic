from modeltranslation.translator import TranslationOptions, register

from .models import Category, Product, SubCategory


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    """
    Переводимые поля модели Category.
    modeltranslation автоматически создаёт поля category_name_ru, category_name_en и т.д.
    в зависимости от LANGUAGES в settings.py
    """

    fields = ("category_name",)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    """
    Переводимые поля модели Product.
    Создаются поля: product_name_ru, product_name_en, description_ru, description_en
    """

    fields = ("product_name", "description")


@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    """
    Переводимые поля модели SubCategory.
    Создаётся поле: sub_category_name_ru, sub_category_name_en
    """

    fields = ("sub_category_name",)
