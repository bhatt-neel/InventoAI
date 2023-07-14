from django.contrib import admin
from .models import *

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'custom_date']

    @staticmethod
    def customer_name(obj):
        return f'{obj.customer.fname} {obj.customer.lname}'


class OrderedProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'costPrice', 'mrp', 'sellingPrice', 'qty', 'tax']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedProducts, OrderedProductAdmin)
