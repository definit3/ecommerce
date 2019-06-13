from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Items(models.Model):
    item_id = models.TextField()
    item_price = models.IntegerField(default=0)
    item_previous_price = models.IntegerField(default=0)
    name = models.TextField(blank=True)
    item_image = models.ImageField(upload_to='item_image', blank=True)
    def __str__(self):
        return self.name + self.item_id

class Sellers(models.Model):
    seller_id = models.TextField()
    seller_name = models.TextField(default=None, null=True)
    seller_tagline = models.TextField(default=None, null=True)
    seller_email = models.EmailField(default=None, null=True)
    seller_address = models.TextField(default="", null=True)
    seller_image = models.ImageField(upload_to='profile_image', blank=True)
    is_buyer = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
    def __str__(self):
        return self.seller_email

class SellersItems(models.Model):
    seller = models.ForeignKey(Sellers,on_delete=models.CASCADE)
    item = models.OneToOneField(Items,on_delete=models.CASCADE,)
    count = models.IntegerField()
    def __str__(self):
        return self.seller.seller_name

class Cart(models.Model):
    item = models.ForeignKey(Items,on_delete=models.CASCADE,)
    count = models.IntegerField()

class Orders(models.Model):
    buyer = models.ForeignKey(Sellers,on_delete=models.CASCADE,)
    order_id = models.TextField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,)
    price = models.IntegerField(default=0)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.order_id
