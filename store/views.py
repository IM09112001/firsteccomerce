from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .utils import cookieCart, cartData, guestOrder

class StoreListView(TemplateView):
    template_name = 'cart.html'


def store(request):
    data = cartData(request)
    products = Product.objects.all()

    items_per_page = request.GET.get('page_count') if request.GET.get('page_count') else 1
    paginator = Paginator(products, items_per_page)

    page = request.GET.get('page')

    try:
        # Get the corresponding page from the paginator
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results.
        products = paginator.page(paginator.num_pages)

    cartItems = data['cartItems']       

    context = {
        'products':products,
        'cartItems': cartItems
        }
    return render(request, 'store.html', context=context)

def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)

def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)

def product_info(request, product_id):
    data = cartData(request)

    cartItems = data['cartItems']

    product = get_object_or_404(Product, id=product_id)
    context = {'cartItems': cartItems,'product': product}
    return render(request, 'product_info.html', context)

def error_404(request, exception):
    return render(request, '404.html', status=404)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Data:', data)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)

# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def proccessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        print('user is not logged in...')
        print('COOKIES:', request.COOKIES)

        customer, order = guestOrder(request=request, data=data)


    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )

    order.save()

    return JsonResponse('Payment submitted...', safe=False)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('store:store') 
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store:store') 
    else:
        form = UserCreationForm()
    return render(request, 'sign_up.html', {'form': form})

def sign_out(request):
    logout(request)
    return redirect('store:store') 