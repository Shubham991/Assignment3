# Import necessary classes
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

from .models import Category, Product, Client, Order
from django.shortcuts import render


# Create your views here.

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index0.html', {'cat_list': cat_list})
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
    return render(request, 'myapp/about0.html')
    # response = HttpResponse()
    # heading1 = '<p>This is an Online Store APP</p>'
    # response.write(heading1)
    # return response


def detail(request, cat_no):
    response = HttpResponse()
    cat = get_object_or_404(Category, id=cat_no)
    prod_list = Product.objects.filter(category=cat_no)
    return render(request, 'myapp/detail0.html',
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
