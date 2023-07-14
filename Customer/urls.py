from django.urls import path
from .views import *

urlpatterns = [
    path('', CustomerView, name="customers"),
]
