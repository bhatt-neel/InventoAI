from django.shortcuts import render
from django.views import View
from django.contrib import messages
from .logic import *
from .validation import *
from Customer.models import Customer
from Product.models import Product

# Create your views here.


class CreateInvoiceView(View):

    def get(self, request):
        customers = Customer.objects.all()
        products = Product.objects.all()
        data = {'title': 'Create Invoices', 'customers': customers, 'products': products, 'invoice': 'active'}
        return render(request, 'Pages/Order/CreateInvoice.html', data)

    def post(self, request):
        customers = Customer.objects.all()
        products = Product.objects.all()

        response = InvoicePostRequestHandler(request)

        if not response['status']:
            messages.error(request, response['error_msg'])

        data = {'title': 'Create Invoices', 'customers': customers, 'products': products, 'invoice': 'active'}

        return render(request, 'Pages/Order/CreateInvoice.html', data)

