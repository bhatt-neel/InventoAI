from django.shortcuts import render
from .models import *

# Create your views here.


def CustomerView(request):
    customers = Customer.objects.all()
    data = {'title': 'Customers', 'customers': customers, 'customer':'active'}
    return render(request, 'Pages/Customer/ViewCustomer.html', data)