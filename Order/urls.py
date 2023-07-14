from django.urls import path
from .views import *

urlpatterns = [
    path('create-invoice/', CreateInvoiceView.as_view(), name="create-invoice"),
]

