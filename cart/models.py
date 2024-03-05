from django.utils import timezone
from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from shopping import settings

class Product(models.Model):
    name = models.CharField(max_length=255, default='Default Name')
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, default='none')
    price = models.CharField(max_length=100) 
    category = models.CharField(max_length=255, default='Uncategorized')
    description = models.TextField()
    image = models.URLField()

    def __str__(self) -> str:
        """
        Get a string representation of the product.

        Returns:
            str: String representation of the product.
        """
        return str(self.name)

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    objects = models.Manager()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)

