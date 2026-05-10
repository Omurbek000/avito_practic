from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


ROLE_CHOICES = (
    ("simple"),
    ("simple"),
    ("bronze"),
    ("bronze"),
    ("silver"),
    ("silver"),
    ("gold"),
    ("gold"),
)


TYPE_CHOICES =(
    ('new'), ('new'),
    ('used'), ('used'),
    ('reserved'), ('reserved'),
    ('sold'), ('sold'),

)

class User(AbstractUser):
    status = models.CharField(max_length=16, choices=ROLE_CHOICES, default="simple")
    phone_number = PhoneNumberField(
        region="KG", null=True, blank=True, verbose_name="Номер телефона"
    )
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(17), MaxValueValidator(70)], null=True, blank=True
    )
    avatar = models.ImageField(upload_to="avatar_image/", null=True, blank=True)
    date_register = models.DateField(auto_now_add=True)


class Cartegory(models.Model):
    category_name = models.CharField(max_length=32, unique=True)
    category_image = models.ImageField(
        upload_to="category_image/", null=True, blank=True
    )

    def __str__(self) -> str:
        return self.category_name


class SubCategory(models.Model):
    category_name = models.ForeignKey(Cartegory, on_delete=models.CASCADE)
    sub_category_image = models.ImageField(
        upload_to="sub_category_image/", null=True, blank=True
    )
    sub_category_name = models.CharField(max_length=32, unique=True)

    def __str__(self) -> str:
        return self.category_name


class Product(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=32)
    product_image = models.ImageField(upload_to="product_image/", null=True, blank=True)
    article_number = models.PositiveBigIntegerField(unique=True, null=True, blank=True)
    price = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    product_type = models.CharField(max_length=6, choices=TYPE_CHOICES, default='new')
    created_data = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product_name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_image')
    product_image = models.ImageField(upload_to="image_product/", null=True, blank=True)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True
    )
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
