from django.urls import path
from myapp import views

app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about', views.about, name='about'),
    path(r'<int:cat_no>', views.detail, name='detail'),
    path(r'products', views.products, name='products'),
    path(r'placeorder', views.place_order, name='placeorder'),
    path(r'products/<int:prod_id>', views.productdetail, name='productdetail'),
]
