from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


ROLE_CHOICES = (
    ("simple", "Simple"),     
    ("bronze", "Bronze"),
    ("silver", "Silver"),
    ("gold", "Gold"),
)

TYPE_CHOICES = (
    ('new', 'New'),             
    ('used', 'Used'),
    ('reserved', 'Reserved'),
    ('sold', 'Sold'),
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

    def __str__(self) :
        return self.status

    def get_user_rating(self):
        ratings = self.user_review.all()
        if ratings.exists():
            return  sum([i.stars for i in ratings]) / ratings.count()
        
        return 0
    
    def get_user_people(self):
        return self.user_review.count()
    
        

class Cartegory(models.Model):
    category_name = models.CharField(max_length=32, unique=True)
    category_image = models.ImageField(
        upload_to="category_image/", null=True, blank=True
    )

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category_name = models.ForeignKey(Cartegory, on_delete=models.CASCADE, related_name='sub_category')
    sub_category_image = models.ImageField(
        upload_to="sub_category_image/", null=True, blank=True
    )
    sub_category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.sub_category_name


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products_owner', null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='sub_category_product')
    product_name = models.CharField(max_length=32)
    article_number = models.PositiveBigIntegerField(unique=True, null=True, blank=True)
    price = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    product_type = models.CharField(max_length=8, choices=TYPE_CHOICES, default='new')
    created_date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.product_name
    
    def get_avg_rating(self):
        ratings = self.product_review.all()
        if ratings.exists():
            return  sum([i.stars for i in ratings]) / ratings.count()
        
        return 0
    
    def get_count_people(self):
        return self.product_review.count()
    


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')  
    product_image = models.ImageField(upload_to="image_product/", null=True, blank=True)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_review')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_review')
    stars = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True
    )
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)