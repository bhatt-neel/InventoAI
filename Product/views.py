from django.shortcuts import render
from .models import *

# Create your views here.


def ProductView(request):
    products = Product.objects.all()
    data = {'title': 'Products', 'products': products, 'product':'active'}
    return render(request, 'Pages/Product/ViewProduct.html', data)