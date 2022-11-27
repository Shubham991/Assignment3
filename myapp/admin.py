from django.contrib import admin
from .models import Product, Category, Client, Order


def add_stock(modeladmin, request, queryset):
    for obj in queryset:
        obj.stock = obj.stock + 50;
        obj.save()

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')
    actions = [add_stock]


class ClientAdmin(admin.ModelAdmin):
    def interested_in(self):
        return " ".join([cat.name for cat in self.interested_in.all()])

    list_display = ('first_name', 'last_name', 'city', interested_in)


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Client, ClientAdmin)
admin.site.register(Order)


