from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=8)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    brand = models.CharField(max_length=100)
    image = models.CharField(max_length=500)
    views = models.PositiveIntegerField(default=0)


class User(models.Model):
    pass
