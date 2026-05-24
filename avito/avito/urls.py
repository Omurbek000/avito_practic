from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



# Swagger / ReDoc — автодокументация API
# Доступна по адресам:
#   /swagger/ — интерактивная документация
#   /redoc/   — читабельная документация


schema_view = get_schema_view(
    openapi.Info(
        title="Avito API",
        default_version="v1",
        description="API для Avito проекта",
    ),
    public=True,
    # Документация доступна всем без авторизации
    permission_classes=[permissions.AllowAny],
)



# URL маршруты


urlpatterns = i18n_patterns(
    # Админ панель Django
    path("admin/", admin.site.urls),

    # Все маршруты приложения store (продукты, корзина, избранное и т.д.)
    path("", include("store.urls")),

    # Маршруты django-allauth (социальная авторизация — Google, GitHub и т.д.)
    path("accounts/", include("allauth.urls")),

) + [
    # Swagger UI — интерактивная документация с возможностью тестировать запросы
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),

    # ReDoc — красивая читабельная документация
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),

# Раздача медиафайлов (аватары, фото товаров) в режиме разработки
# В продакшене медиафайлы должны раздаваться через Nginx, а не Django
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# urlpatterns = [
 
#     # ── API маршруты (без языкового префикса) ──
#     # React обращается сюда напрямую: /login/, /products/, /cart/ и т.д.
#     path('', include('store.urls')),
 
#     # Документация API
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
 
# ] + i18n_patterns(
 
#     # ── Маршруты с языковым префиксом (/ru/admin/, /en/admin/) ──
#     path('admin/', admin.site.urls),
#     path('accounts/', include('allauth.urls')),
 
# ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 