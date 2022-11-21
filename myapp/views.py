# Import necessary classes
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

from .forms import OrderForm, InterestForm
from .models import Category, Product, Client, Order
from django.shortcuts import render


# Create your views here.

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    username = "User"
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'username': username})
    # cat_list = Category.objects.all().order_by('id')[:10]
    # response = HttpResponse()
    # heading1 = '<p>' + 'List of categories: ' + '</p>'
    # response.write(heading1)
    # for category in cat_list:
    #     para = '<p>' + str(category.id) + ': ' + str(category) + '</p>'
    #     response.write(para)
    #
    # prod_list = Product.objects.all().order_by('-price')[:5]
    # heading2 = '<p>' + 'List of Products: ' + '</p>'
    # response.write(heading2)
    # for product in prod_list:
    #     para = '<p>' + str(product.id) + ': ' + str(product) + ' Price: ' + str(product.price) + '</p>'
    #     response.write(para)
    # return response


def about(request):
    return render(request, 'myapp/about.html')
    # response = HttpResponse()
    # heading1 = '<p>This is an Online Store APP</p>'
    # response.write(heading1)
    # return response


def detail(request, cat_no):
    response = HttpResponse()
    cat = get_object_or_404(Category, id=cat_no)
    prod_list = Product.objects.filter(category=cat_no)
    return render(request, 'myapp/detail.html',
                  {'cat': cat,
                   'prod_list': prod_list})

    # heading = '<p> Category: ' + str(cat.name) + '</p>'
    # response.write(heading)
    # heading = '<p> Warehouse Location: ' + str(cat.warehouse) + '</p>'
    # response.write(heading)
    # prod_list = Product.objects.filter(category=cat_no)
    # heading = '<p> List of Products: </p>'
    # response.write(heading)
    # for product in prod_list:
    #     response.write('<p> '+str(product)+'</p>')
    # return response


def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                msg = 'Your order has been placed successfully.'

                order.product.stock -= order.num_units
                order.product.save()
                if order.product.stock < 100:
                    order.product.refill()
            else:
                msg = 'We do not have sufficient stock to fill your order.'

            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form':form, 'msg':msg, 'prodlist':prodlist})


def productdetail(request, prod_id):
    prod = get_object_or_404(Product, id=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            if form.cleaned_data['interested'] == '1':
                prod.interested += 1
                prod.save()
            return index(request)

    else:
        form = InterestForm()
        return render(request, 'myapp/productdetail.html', {'prod': prod, 'form': form})
