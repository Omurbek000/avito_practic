from django.contrib import admin
from modeltranslation.admin import TranslationAdmin


from .models import User, Category, SubCategory, Product, ProductImage, Review



# Медиафайлы для tabbed интерфейса переводов в админке
# Добавляет вкладки RU / EN / KY при редактировании переводимых полей


TRANSLATION_MEDIA = {
    'js': (
        '/static/modeltranslation/js/force_jquery.js',
        'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
        '/static/modeltranslation/js/tabbed_translation_fields.js',
    ),
    'css': {
        'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
    },
}



# Inline — вложенные модели внутри страницы редактирования


class ProductImageInline(admin.TabularInline):
    """Фотографии товара — редактируются прямо на странице товара."""

    model = ProductImage
    # extra=1 — одно пустое поле для добавления новой фотографии
    extra = 1


class ReviewInline(admin.TabularInline):
    """Отзывы на товар — только для просмотра, редактировать нельзя."""

    model = Review
    # extra=0 — не показываем пустые поля для новых отзывов
    extra = 0
    # Все поля только для чтения — отзывы не должны редактироваться из товара
    readonly_fields = ['user', 'stars', 'comment', 'created_date']



# Регистрация моделей в админке


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Управление пользователями."""

    list_display = ['username', 'email', 'status', 'age', 'phone_number', 'date_register']
    list_filter = ['status']
    search_fields = ['username', 'email']



@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    """
    Категории товаров с поддержкой переводов.
    TranslationAdmin добавляет вкладки RU / EN / KY для переводимых полей.
    """

    list_display = ['category_name']
    search_fields = ['category_name']

    class Media:
        js = TRANSLATION_MEDIA['js']
        css = TRANSLATION_MEDIA['css']


@admin.register(SubCategory)
class SubCategoryAdmin(TranslationAdmin):
    """Подкатегории с поддержкой переводов."""

    list_display = ['sub_category_name', 'category_name']
    list_filter = ['category_name']
    search_fields = ['sub_category_name']

    class Media:
        js = TRANSLATION_MEDIA['js']
        css = TRANSLATION_MEDIA['css']


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    """
    Товары с поддержкой переводов.
    Включает inline редактирование фото и просмотр отзывов.
    """

    list_display = ['product_name', 'price', 'product_type', 'sub_category', 'owner', 'created_date']
    list_filter = ['product_type', 'sub_category']
    search_fields = ['product_name', 'article_number']
    readonly_fields = ['created_date']
    # Фото и отзывы редактируются прямо на странице товара
    inlines = [ProductImageInline, ReviewInline]

    class Media:
        js = TRANSLATION_MEDIA['js']
        css = TRANSLATION_MEDIA['css']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Фотографии товаров."""

    list_display = ['product', 'product_image']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы на товары."""

    list_display = ['product', 'user', 'stars', 'created_date']
    list_filter = ['stars']
    search_fields = ['product__product_name', 'user__username']
    readonly_fields = ['created_date']



# Кастомизация шапки админки


admin.site.index_title = "Avito — Управление"
admin.site.site_title = "Avito Admin"
admin.site.site_header = "Avito"
