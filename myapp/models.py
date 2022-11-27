from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=200, default='Any String', blank=False)

    def __str__(self):
        return self.name


def validate_stock(value):
    if value < 0 or value > 1000:
        raise ValidationError("The stock must be between 0 to 1000.")


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100, validators=[validate_stock])
    available = models.BooleanField(default=True)
    optional = models.CharField(max_length=300, default='', blank=True)
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def refill(self):
        self.stock += 100
        self.save()
        return


class Client(User):
    PROVINCE_CHOICES = [
        ('AB', 'Alberta'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'), ]

    company = models.CharField(max_length=50, blank=True)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)
    profile_pic = models.ImageField(upload_to='uploads/', null=True)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField()
    STATUS_CHOICES = [
        (0, 'Order Cancelled'),
        (1, 'Order Placed'),
        (2, 'Order Shipped'),
        (3, 'Order Delivered')]
    order_status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    status_date = models.DateField(null=True)

    def __str__(self):
        return self.product.name + 'x' + str(self.num_units)

    def total_cost(self):
        return self.product.price * self.num_units
