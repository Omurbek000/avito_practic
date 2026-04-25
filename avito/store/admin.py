from django.contrib import admin
from .models import User, Cartegory, SubCategory, Product, ProductImage, Review
from modeltranslation.admin import TranslationAdmin


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Cartegory, SubCategory)
class ModelAdmin(TranslationAdmin):

    class Media:
        js = (
            "/static/modeltranslation/js/force_jquery.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js",
            "/static/modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("/static/modeltranslation/css/tabbed_translation_fields.css",),
        }


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    inlines = [ProductImageInline]

    class Media:
        js = (
            "/static/modeltranslation/js/force_jquery.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js",
            "/static/modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("/static/modeltranslation/css/tabbed_translation_fields.css",),
        }



admin.site.register(User)
admin.site.register(Review)