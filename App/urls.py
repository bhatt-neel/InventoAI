from django.urls import path, include
from .views import *

urlpatterns = [
    path('', IndexPage.as_view(), name="homepage"),
    path('products/', include('Product.urls')),
    path('customers/', include('Customer.urls')),
    path('order/', include('Order.urls')),
]
