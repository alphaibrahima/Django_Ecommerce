from itertools import product
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required



# Function for request session key of session active or if not exist then create cart
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(user=current_user, product=product)
            cart_item.quantite += 1
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                user = current_user,
                product = product,
                quantite = 1
            )
        cart_item.save()
        return redirect('cart')
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantite += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantite = 1
            )
            cart_item.save()
        return redirect('cart')



# allow the customer to reduce the quantity of his order
def remove_cart(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)
    if current_user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=current_user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantite > 1:
        cart_item.quantite -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, product_id):
    
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)

    if current_user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=current_user)  
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

# 
def cart(request, total = 0, quantity = 0, cart_items = None):
    try:
        tax = 0
        global_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantite)
            quantity += cart_item.quantite
        tax = (2 * total)/100
        print(tax)
        global_total = tax + total
    except ObjectDoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'global_total': global_total
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total = 0, quantity = 0, cart_items = None):
    try:
        tax = 0
        global_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantite)
            quantity += cart_item.quantite
        tax = (2 * total)/100
        print(tax)
        global_total = tax + total
    except ObjectDoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'global_total': global_total
    }
    return render (request, 'store/checkout.html', context)