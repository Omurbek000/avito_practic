from pathlib import Path
from datetime import timedelta
import os

from dotenv import load_dotenv




# Базовые пути


BASE_DIR = Path(__file__).resolve().parent.parent

# Загружаем переменные окружения из файла .env
load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-change-in-production')

# В продакшене обязательно DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ['*']


# Приложения


INSTALLED_APPS = [
    # modeltranslation  для языка
    'modeltranslation',

    # Стандартные Django приложения
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Нужно для allauth
    'django.contrib.sites',

    # Наше приложение
    'store',

    # DRF и фильтры
    'rest_framework',
    'django_filters',
    'phonenumber_field',

    # Авторизация через соцсети
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',

    
    'drf_yasg',

    # JWT токены
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    
    #front
    'corsheaders',
]



# Middleware


MIDDLEWARE = [
    #front
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # LocaleMiddleware — для переключения языков (i18n)
    # Должен стоять ПОСЛЕ SessionMiddleware и ДО CommonMiddleware
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'avito.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'avito.wsgi.application'



# База данных



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL для продакшена — раскомментируй когда будешь деплоить

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME', 'avito'),
#         'USER': os.getenv('DB_USER', 'postgres'),
#         'PASSWORD': os.getenv('DB_PASSWORD', ''),
#         'HOST': os.getenv('DB_HOST', 'localhost'),
#         'PORT': os.getenv('DB_PORT', '5432'),
#     }
# }



# Валидация паролей


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]



# Интернационализация (i18n)


LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True  
USE_TZ = True

# Поддерживаемые языки
LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
    ('ky', 'Kyrgyz'),
)

# Настройки modeltranslation
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_LANGUAGES = ('ru', 'en', 'ky')

# Папка с файлами переводов (.po/.mo файлы)
LOCALE_PATHS = [BASE_DIR / 'locale']



# Статика и медиафайлы


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'






# Говорим Django использовать нашу модель User вместо стандартной
AUTH_USER_MODEL = 'store.User'

# Нужно для django.contrib.sites и allauth
SITE_ID = 1

# Чтобы Django не выдавал предупреждения о типе первичного ключа
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Django REST Framework


REST_FRAMEWORK = {
    # Фильтрация через django-filters по всему проекту
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    # JWT авторизация по умолчанию
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}



# JWT (Simple JWT)


SIMPLE_JWT = {
    # access токен живёт 5 минут — для разработки можно увеличить до 60
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    # refresh токен живёт 1 день
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # При обновлении токена — выдаём новый refresh токен
    'ROTATE_REFRESH_TOKENS': True,
    # Старый refresh токен после rotation добавляется в blacklist
    'BLACKLIST_AFTER_ROTATION': True,
    # Обновляем last_login при каждом получении токена
    'UPDATE_LAST_LOGIN': True,
    # Тип токена в заголовке: Authorization: Bearer <token>
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    # ИСПРАВЛЕНО: убран 'AUTO_TOKEN_ENADLE' — такого параметра не существует (опечатка)
}



# Allauth (авторизация через соцсети)


AUTHENTICATION_BACKENDS = [
    # Стандартная авторизация Django (логин/пароль)
    'django.contrib.auth.backends.ModelBackend',
    # Авторизация через allauth (Google, GitHub)
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Используем email как основной идентификатор
ACCOUNT_LOGIN_METHODS = {'email'}  # вход по email
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

# Письма выводятся в консоль (для разработки)
# В продакшене заменить на реальный SMTP
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Vite работает на 5173, не 3000
]