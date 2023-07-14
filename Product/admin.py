from django.contrib import admin
from .models import *

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sellingPrice']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
