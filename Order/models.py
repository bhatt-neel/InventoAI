from django.db import models
from Base.models import BaseModel
from Product.models import Product
from Customer.models import Customer

# Create your models here.


class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    custom_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.fname} {self.customer.lname}'


class OrderedProducts(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    costPrice = models.IntegerField()
    mrp = models.IntegerField()
    sellingPrice = models.IntegerField()
    qty = models.IntegerField()
    tax = models.IntegerField()

    def __str__(self):
        return self.product.name