
from django.db import models
from django.forms import CharField

# Create your models here.

class Seller(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)  # Foreignkey
    name = models.CharField(max_length=50)
    des = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField(default=0)
    pic = models.FileField(upload_to='products',default='avatar.png')
    discount = models.IntegerField()

    def __str__(self):
        return self.name
