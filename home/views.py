from multiprocessing import context
from pyexpat import model
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
from django.views.generic import DetailView
# Create your views here.

def index(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        "products": products,
    }
    return render(request, 'home/index.html', context)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'home/product-detail.html'




def about(request):
    return render(request, 'home/about.html')