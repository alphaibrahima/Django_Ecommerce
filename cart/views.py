from django.shortcuts import render
from store.models import Product
from .models import Cart, CartItem



def cart(request):
    return render(request, 'store/cart.html')