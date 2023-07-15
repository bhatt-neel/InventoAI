from django.urls import path
from .views import *

urlpatterns = [
    path('create-invoice/', CreateInvoiceView.as_view(), name="create-invoice"),
    path('get_customer/', get_customer, name="get-customer")
]

