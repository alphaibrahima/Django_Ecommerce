from itertools import product
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist



# Function for request session key of session active or if not exist then create cart
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    try :
        # try recuperate the card that has id equals to _cart_id
        cart = Cart.objects.get(cart_id=_cart_id(request))
    #  if this cart not exist we create one
    except Cart.DoesNotExist :
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try :
        cart_item = CartItem.objects.get(product=product, cart=cart )
        cart_item.quantite +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantite = 1,
            cart = cart
        )
    return redirect('cart')


def cart(request, total = 0, quantity = 0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantite)
            quantity += cart_item.quantite
    except ObjectDoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items
    }
    return render(request, 'store/cart.html', context)