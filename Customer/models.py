from django.db import models
from Base.models import BaseModel, Country, State, City
from smart_selects.db_fields import ChainedForeignKey


# Create your models here.


class Customer(BaseModel):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.fname} {self.lname}'