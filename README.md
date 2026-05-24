<div align="center">

# 🛍️ Авито — Учебный проект

**Полноценный маркетплейс объявлений с REST API, JWT авторизацией и React фронтендом**

![Django](https://img.shields.io/badge/Django-4.x-092E20?style=for-the-badge&logo=django)
![DRF](https://img.shields.io/badge/DRF-3.x-ff1709?style=for-the-badge)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)

</div>

---

## 📋 О проекте

Учебный проект — клон Авито. Пользователи могут размещать объявления, добавлять товары в корзину и избранное, оставлять отзывы. Проект сделан для практики бэкенд разработки на Django DRF с React фронтендом.

> ⚠️ **Статус:** В разработке. Некоторые функции ещё не реализованы (см. раздел TODO).

---

## ✅ Реализовано

- [x] Регистрация и авторизация по email (JWT)
- [x] Кастомная модель пользователя
- [x] Категории и подкатегории товаров
- [x] Список товаров с фильтрацией, поиском, сортировкой и пагинацией
- [x] Детальная страница товара с рейтингом
- [x] Корзина и избранное
- [x] Отзывы на товары
- [x] Загрузка фото товаров
- [x] Мультиязычность (RU / EN / KY) через modeltranslation
- [x] Swagger документация API
- [x] React фронтенд с тёмной темой

## 🚧 TODO (не готово)

- [ ] Вход через Google и GitHub (OAuth настроен, нужны credentials)
- [ ] Страница профиля пользователя
- [ ] Чат между продавцом и покупателем
- [ ] Деплой на сервер (Nginx + Gunicorn + Docker)
- [ ] Push уведомления

---

## 🗂️ Структура проекта

```
avito_practic/
├── avito/                  # Конфигурация Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                  # Основное приложение
│   ├── models.py           # Модели БД
│   ├── serializers.py      # DRF сериализаторы
│   ├── views.py            # Вьюхи
│   ├── urls.py             # URL маршруты
│   ├── filters.py          # Фильтры
│   ├── pagination.py       # Пагинация
│   ├── permissions.py      # Права доступа
│   ├── admin.py            # Админ панель
│   └── translation.py      # Переводы
├── avito-frontend/         # React приложение
│   └── src/
│       ├── pages/          # Страницы
│       ├── components/     # Компоненты
│       ├── api/            # Axios настройка
│       └── utils/          # Утилиты
├── create_test_data.py     # Скрипт тестовых данных
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Установка и запуск

### Требования
- Python 3.11+
- Node.js 18+
- pip

### Бэкенд

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Omurbek000/avito_practic.git
cd avito_practic

# 2. Создать виртуальное окружение
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Создать .env файл
echo "SECRET_KEY=your-secret-key-here" > .env

# 5. Применить миграции
python manage.py makemigrations
python manage.py migrate

# 6. Заполнить тестовыми данными
python manage.py shell < create_test_data.py

# 7. Запустить сервер
python manage.py runserver
```

### Фронтенд

```bash
cd avito-frontend
npm install
npm run dev
```

### Готово!
| Сервис | URL |
|--------|-----|
| 🖥️ Фронтенд | http://localhost:5173 |
| 🔧 API | http://localhost:8000 |
| 📚 Swagger | http://localhost:8000/swagger/ |
| ⚙️ Админка | http://localhost:8000/ru/admin/ |

---

## 🔑 Тестовые аккаунты

| Email | Пароль | Роль |
|-------|--------|------|
| admin@admin.com | admin | Суперпользователь |
| user1@admin.com | admin | Пользователь Bronze |
| user2@admin.com | admin | Пользователь Silver |

---

## 📡 API Эндпоинты

### Авторизация
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/register/` | Регистрация |
| POST | `/login/` | Вход (возвращает JWT) |
| POST | `/logout/` | Выход |

### Товары
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/products/` | Список товаров |
| POST | `/products/` | Создать товар 🔒 |
| GET | `/products/<id>/` | Детали товара |

### Параметры фильтрации
```
/products/?search=iPhone          # поиск по названию
/products/?product_type=new       # фильтр по типу
/products/?ordering=-price        # сортировка по цене
/products/?price__gt=1000         # цена больше 1000
/products/?price__lt=50000        # цена меньше 50000
/products/?page=2&page_size=12    # пагинация
```

### Корзина
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/cart/` | Корзина пользователя 🔒 |
| POST | `/cart_item/` | Добавить в корзину 🔒 |
| DELETE | `/cart_item/<id>/` | Удалить из корзины 🔒 |

> 🔒 Требует JWT токен: `Authorization: Bearer <access_token>`

---

## 🛠️ Технологии

**Бэкенд:**
- Django 4.x + Django REST Framework
- PostgreSQL / SQLite
- Simple JWT — авторизация
- django-allauth — OAuth (Google, GitHub)
- django-modeltranslation — мультиязычность
- django-filters — фильтрация
- drf-yasg — Swagger документация
- Pillow — работа с изображениями

**Фронтенд:**
- React 18 + Vite
- React Router DOM
- Axios
- Google Fonts (Unbounded, Inter)

---

## 👨‍💻 Автор

**Omurbek** — Backend Python Developer (в процессе обучения)

- GitHub: [@Omurbek000](https://github.com/Omurbek000)

---

<div align="center">
  <sub>Проект создан в учебных целях 🎓</sub>
</div>
