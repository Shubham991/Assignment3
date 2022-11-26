from django.contrib import admin
from .models import Product, Category, Client, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'interested_in')


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Order)


