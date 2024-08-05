from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import json
from .utils import * 
from django.http import JsonResponse
from .models import *
from django.contrib.auth import login, authenticate, logout


# Create your views here.
def store (request):
    cookieData =  cart_data(request)
    cart_items = cookieData['cart_items']
    order = cookieData['order']
    items = cookieData['items']
    context = {
        'products' : Product.objects.all(),
        'order': order,
        'items': items,
        'cart_items': cart_items}
    return render (request, 'store/store.html', context )

def electronics(request):
    cookieData =  cart_data(request)
    cart_items = cookieData['cart_items']
    order = cookieData['order']
    items = cookieData['items']
    context = {
        'products' : Product.objects.filter(category = 1),
        'order': order,
        'items': items,
        'cart_items': cart_items}
    return render (request, 'store/electronics.html', context )

def clothing(request):
    cookieData =  cart_data(request)
    cart_items = cookieData['cart_items']
    order = cookieData['order']
    items = cookieData['items']
    context = {
        'products' : Product.objects.filter(category = 2),
        'order': order,
        'items': items,
        'cart_items': cart_items}
    return render (request, 'store/clothing.html', context )

def shoes(request):
    cookieData =  cart_data(request)
    cart_items = cookieData['cart_items']
    order = cookieData['order']
    items = cookieData['items']
    context = {
        'products' : Product.objects.filter(category = 3),
        'order': order,
        'items': items,
        'cart_items': cart_items}
    return render (request, 'store/shoes.html', context )

def palestine(request):
    cookieData =  cart_data(request)
    cart_items = cookieData['cart_items']
    order = cookieData['order']
    items = cookieData['items']
    context = {
        'products' : Product.objects.filter(category = 5),
        'order': order,
        'items': items,
        'cart_items': cart_items}
    return render (request, 'store/palestine.html', context )

def cart (request):
    cookieData =  cart_data(request)
    cart_items = cookieData['cart_items']
    order = cookieData['order']
    items = cookieData['items']
    context = {
        'products' : Product.objects.all(),
        'order': order,
        'items': items,
        'cart_items': cart_items}
    return render (request, 'store/cart.html', context)

def product (request, product_id):
    product = get_object_or_404(Product, id = product_id)
    cookieData =  cart_data(request)
    cart_items = cookieData['cart_items']
    order = cookieData['order']
    items = cookieData['items']
    context = {
        'product': product,
        'products': Product.objects.filter(category = product.category).exclude(id = product_id).order_by('?')[:4],
        'order': order,
        'items': items,
        'cart_items': cart_items}
    return render (request, 'store/product.html', context)

def checkout (request):
    cookieData =  cart_data(request)
    cart_items = cookieData['cart_items']
    order = cookieData['order']
    items = cookieData['items']
    
    context = {
        'product': Product.objects.all(),
        'order': order,
        'items': items,
        'cart_items':cart_items
    }
    return render (request, 'store/checkout.html', context)

def updateItems(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('action:', action)
    print('product:', productId)
    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
        print ('item was deleted')
    return JsonResponse ('Item was added', safe=False)

def processOrder(request):
    try:
        transactionId = datetime.now().timestamp()
        data = json.loads(request.body)
        user_info = data['userInfo']
        shipping_info = data['shippingInfo']
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer = customer, complete = False)
        else:
          order, customer = guestOrder(request, data)
        if order.shipping == True:
            shippingAddress.objects.create(
                customer = customer,
                order = order,
                address = shipping_info['address'],
                city = shipping_info['city'],
                state = shipping_info['state'],
                zipcode = shipping_info['zipcode']
            )
        total = float(user_info['total'])
        order.transaction_id = transactionId
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        return JsonResponse('Payment complete', safe=False)
    except Exception as e:
        return JsonResponse({'Error': str(e)})

def signIn(request):
    cookieData =  cart_data(request)
    cart_items = cookieData['cart_items']
    order = cookieData['order']
    items = cookieData['items']
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect("store")

        else:
            return render(request, 'store/signin.html', {'error': 'Incorrect password', 'cart_items': cart_items}) 
    except:
        pass      

    context = {
        'products' : Product.objects.all(),
        'order': order,
        'items': items,
        'cart_items': cart_items}
    return render (request, 'store/signin.html', context)

def signUp(request):
    cookieData =  cart_data(request)
    cart_items = cookieData['cart_items']
    order = cookieData['order']
    items = cookieData['items']

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        
        if  User.objects.filter(username = username).exists():
            return render(request, 'store/signup.html', {'error': 'Username already exists', 'cart_items': cart_items, })
        elif User.objects.filter(email = email).exists():
            return render(request, 'store/signup.html', {'error': 'Email already exists', 'cart_items': cart_items})     
        
        try:
            user = User.objects.create_user(username = username, email = email, password = password)   
            customer = Customer.objects.create(user = user, email = email, name = name) 
            login(request, user)
            return redirect("store")
        except:
            return render(request, 'store/signup.html', {'error': 'An error occurred while creating the account', 'cart_items': cart_items})

    

    context = {
        'products' : Product.objects.all(),
        'order': order,
        'items': items,
        'cart_items': cart_items, 
        'username': User.objects.all()
        }
    return render (request, 'store/signup.html', context)

def signOut(request):
    logout(request)
    return redirect('store')

