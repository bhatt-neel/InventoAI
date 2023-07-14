from django import template
from Order.logic import *
from django.contrib import messages

register = template.Library()


@register.filter(name="get_product_by_uuid")
def get_product_by_uuid(uuid):
    product = GetProduct.by_uuid(uuid)
    if product['status']:
        return product['object']
    return product


@register.filter(name="get_value_from_key")
def get_value_from_key(dict, key):
    return dict[key]


@register.filter(name="addition")
def addition(num1, num2):
    return num1 + num2


@register.filter(name="multiply")
def multiply(num1, num2):
    return num1*num2


@register.filter(name="GetTotalFromInvoiceSession")
def GetTotalFromInvoiceSession(request):
    response = InvoiceSession.GetTotal(request)
    if response['status']:
        return response['Total']
    else:
        messages.error(request, response['error_msg'])
        return 0

