from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from templatetags.custom_filter import *
from django.contrib import messages
from .logic import *
from .validation import *
from Customer.models import Customer
from Product.models import Product
import json

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


def get_customer(request):
    uuid = request.GET.get('uuid')
    customer = Customer.objects.filter(uuid = uuid)[0]

    response_data = {
        'fname': customer.fname,
        'lname': customer.lname,
        'phone': customer.phone,
        'email': customer.email,
        'address': customer.address
    }

    print(response_data)

    return HttpResponse(json.dumps(response_data), content_type='application/json')

