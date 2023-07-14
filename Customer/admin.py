from django.contrib import admin
from .models import *

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['fname', 'lname']

admin.site.register(Customer, CustomerAdmin)
