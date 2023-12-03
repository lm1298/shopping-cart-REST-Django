from django.utils import timezone
from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Product(models.Model):
    """
    A class representing a product in the online store.

    Fields:
    - name: The name of the product.
    - description: A description of the product (optional).
    - price: The price of the product.
    - image: An image representing the product (optional).
    - is_available: A flag indicating whether the product is currently available.
    - created_at: The timestamp when the product was created.
    - modified_at: The timestamp when the product was last modified.
    - id: A unique identifier for the product.

    Methods:
    - __str__: Get a string representation of the product.

    Reference:
    https://dev.to/nick_langat/building-a-shopping-cart-using-django-rest-framework-54i0
    """
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    id = models.BigAutoField(primary_key=True)

    def __str__(self) -> str:
        """
        Get a string representation of the product.

        Returns:
            str: String representation of the product.
        """
        return str(self.name)
