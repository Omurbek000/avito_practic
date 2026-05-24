from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator



# Константы / Choices

# Статусы пользователя (уровень подписки)
ROLE_CHOICES = (
    ("simple", "Simple"),
    ("bronze", "Bronze"),
    ("silver", "Silver"),
    ("gold", "Gold"),
)

# Состояние товара
TYPE_CHOICES = (
    ("new", "New"),
    ("used", "Used"),
    ("reserved", "Reserved"),
    ("sold", "Sold"),
)


# Пользователь


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Расширяет стандартный AbstractUser дополнительными полями:
    статус подписки, телефон, возраст, аватар.
    """

    status = models.CharField(
        max_length=16,
        choices=ROLE_CHOICES,
        default="simple",
        verbose_name="Статус",
    )
    phone_number = PhoneNumberField(
        region="KG",
        null=True,
        blank=True,
        verbose_name="Номер телефона",
    )
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(17), MaxValueValidator(70)],
        null=True,
        blank=True,
        verbose_name="Возраст",
    )
    avatar = models.ImageField(
        upload_to="avatar_image/",
        null=True,
        blank=True,
        verbose_name="Аватар",
    )
    date_register = models.DateField(auto_now_add=True, verbose_name="Дата регистрации")

    def __str__(self):
        return self.username

    def get_user_rating(self):
        """Возвращает средний рейтинг пользователя на основе отзывов."""
        ratings = self.user_review.all()
        if ratings.exists():
            return sum(i.stars for i in ratings) / ratings.count()
        return 0

    def get_user_people(self):
        """Возвращает количество отзывов об этом пользователе."""
        return self.user_review.count()



# Категории


class Category(models.Model):
    """
    Основная категория товаров (например: Электроника, Одежда).
    """

    category_name = models.CharField(
        max_length=32,
        unique=True,
        verbose_name="Название категории",
    )
    category_image = models.ImageField(
        upload_to="category_image/",
        null=True,
        blank=True,
        verbose_name="Изображение категории",
    )

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(models.Model):
    """
    Подкатегория товаров, привязанная к основной категории
    (например: Смартфоны → Электроника).
    """

    category_name = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="sub_category",
        verbose_name="Категория",
    )
    sub_category_name = models.CharField(
        max_length=32,
        unique=True,
        verbose_name="Название подкатегории",
    )
    sub_category_image = models.ImageField(
        upload_to="sub_category_image/",
        null=True,
        blank=True,
        verbose_name="Изображение подкатегории",
    )

    def __str__(self):
        return self.sub_category_name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


# Товар


class Product(models.Model):
    """
    Модель товара/объявления.
    Каждый товар принадлежит подкатегории и владельцу (owner).
    """

    sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="sub_category_product",
        verbose_name="Подкатегория",
    )
    # Владелец объявления — пользователь который его создал
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
        verbose_name="Владелец",
    )
    product_name = models.CharField(max_length=32, verbose_name="Название товара")
    article_number = models.PositiveBigIntegerField(
        unique=True,
        null=True,
        blank=True,
        verbose_name="Артикул",
    )
    price = models.PositiveIntegerField(verbose_name="Цена")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    product_type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICES,
        default="new",
        verbose_name="Состояние",
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.product_name

    def get_avg_rating(self):
        """Возвращает средний рейтинг товара на основе отзывов."""
        ratings = self.product_review.all()
        if ratings.exists():
            return sum(i.stars for i in ratings) / ratings.count()
        return 0

    def get_count_people(self):
        """Возвращает количество отзывов на товар."""
        return self.product_review.count()

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(models.Model):
    """
    Изображения товара. Один товар может иметь несколько фотографий.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Товар",
    )
    product_image = models.ImageField(
        upload_to="image_product/",
        null=True,
        blank=True,
        verbose_name="Фото товара",
    )

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фото товаров"



# Отзывы


class Review(models.Model):
    """
    Отзыв пользователя на товар.
    Содержит оценку (1-5 звёзд) и текстовый комментарий.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_review",
        verbose_name="Товар",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_review",
        verbose_name="Пользователь",
    )
    stars = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        null=True,
        blank=True,
        verbose_name="Оценка",
    )
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")

    def __str__(self):
        return f"{self.user} — {self.product} ({self.stars}★)"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"



# Корзина


class Cart(models.Model):
    """
    Корзина пользователя. У каждого пользователя одна корзина (OneToOne).
    Создаётся автоматически при первом обращении.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    def get_total_price(self):
        """Возвращает общую сумму всех товаров в корзине."""
        
        return sum(i.get_total_price() for i in self.cart_item.all())

    def __str__(self):
        return f"Корзина пользователя: {self.user}"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class CartItem(models.Model):
    """
    Позиция в корзине. Хранит товар и количество единиц.
    """

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cart_item",
        verbose_name="Корзина",
    )
    
    product_cart = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
    )
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="Количество")

    def get_total_price(self):
        """Возвращает стоимость позиции (цена × количество)."""
       
        return self.quantity * self.product_cart.price

    def __str__(self):
        return f"{self.product_cart} × {self.quantity}"

    class Meta:
        verbose_name = "Позиция корзины"
        verbose_name_plural = "Позиции корзины"



# Избранное


class Favorite(models.Model):
    """
    Список избранных товаров пользователя.
    У каждого пользователя один список (OneToOne).
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    def __str__(self):
        return f"Избранное пользователя: {self.user}"

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"


class FavoriteItem(models.Model):
    """
    Конкретный товар в списке избранного.
    """

    favorite = models.ForeignKey(
        Favorite,
        on_delete=models.CASCADE,
        related_name="favorite_item",
        verbose_name="Список избранного",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
    )

    def __str__(self):
        return f"{self.product} в избранном у {self.favorite.user}"

    class Meta:
        verbose_name = "Товар в избранном"
        verbose_name_plural = "Товары в избранном"
        # Один товар не может быть дважды в избранном у одного пользователя
        unique_together = ("favorite", "product")
