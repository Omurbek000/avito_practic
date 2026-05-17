from django.contrib import admin
from .models import User, Cartegory, SubCategory, Product, ProductImage, Review
from modeltranslation.admin import TranslationAdmin


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


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['user', 'stars', 'comment', 'created_date']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'status', 'age', 'phone_number', 'date_register']
    list_filter = ['status']
    search_fields = ['username', 'email']


@admin.register(Cartegory)
class CategoryAdmin(TranslationAdmin):
    list_display = ['category_name']
    search_fields = ['category_name']

    class Media:
        js = TRANSLATION_MEDIA['js']
        css = TRANSLATION_MEDIA['css']


@admin.register(SubCategory)
class SubCategoryAdmin(TranslationAdmin):
    list_display = ['sub_category_name', 'category_name']
    list_filter = ['category_name']
    search_fields = ['sub_category_name']

    class Media:
        js = TRANSLATION_MEDIA['js']
        css = TRANSLATION_MEDIA['css']


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ['product_name', 'price', 'product_type', 'sub_category', 'created_date']
    list_filter = ['product_type', 'sub_category']
    search_fields = ['product_name', 'article_number']
    readonly_fields = ['created_date']
    inlines = [ProductImageInline, ReviewInline]

    class Media:
        js = TRANSLATION_MEDIA['js']
        css = TRANSLATION_MEDIA['css']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'product_image']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'stars', 'created_date']
    list_filter = ['stars']
    search_fields = ['product__product_name', 'user__username']
    readonly_fields = ['created_date']
    
    
    
# admin.site.index_title = "Avito Premium — Управление"
# admin.site.site_title = "Avito Admin"
# admin.site.site_header = "Avito Premium"    