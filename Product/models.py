from django.db import models
from Base.models import BaseModel

# Create your models here.


class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(BaseModel):
    img = models.ImageField(upload_to='static/img/App/ProductImg/', default='static/img/App/ProductImg/default.png')
    name = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    costPrice = models.IntegerField()
    mrp = models.IntegerField()
    sellingPrice = models.IntegerField()
    qty = models.IntegerField()
    tax = models.IntegerField()
    barcode = models.CharField(max_length=255, unique=True, null=True, blank=True)
    is_deleted = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.name
