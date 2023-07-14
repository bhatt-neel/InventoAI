import uuid
from django.db import models
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(models.Model):
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.country


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.CharField(max_length=255)

    def __str__(self):
        return self.state


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = ChainedForeignKey(State, chained_field="country", chained_model_field="country", show_all=False, auto_choose=True, sort=True)
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.city

