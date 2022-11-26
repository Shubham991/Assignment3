# Import necessary classes
from datetime import datetime

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .forms import OrderForm, InterestForm
from .models import Category, Product, Client, Order
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    username = "User"
    if request.user.is_authenticated:
        username = request.user.username

    lastlogininfo = 'Your last login was more than one hour ago'
    last_login = request.session.get('last_login', False)
    if last_login:
        last_login_datetime = datetime.strptime(last_login, "%d/%m/%Y %H:%M:%S")
        duration = datetime.now() - last_login_datetime
        if duration.seconds < 60 * 60:
            lastlogininfo = last_login

    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'username': username, 'lastlogininfo': lastlogininfo})
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
    numvisits = request.COOKIES.get('about_visits')
    if numvisits:
        numvisits = int(numvisits) + 1
    else:
        numvisits = 1
    response = render(request, 'myapp/about.html', {'numvisits': numvisits})
    response.set_cookie(key='about_visits', value=numvisits, max_age=5 * 60)
    return response
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
        return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


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


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                request.session.set_expiry(60*60)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


@login_required
def myorders(request):
    if Client.objects.filter(username=request.user.username):
        orderlist = Order.objects.filter(client=Client.objects.get(username=request.user.username))
        return render(request, 'myapp/myorders.html', {'user': request.user.username, 'orderlist': orderlist})
    else:
        return HttpResponse('You are not a registered client!')
