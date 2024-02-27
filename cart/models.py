from django.utils import timezone
from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Product(models.Model):
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
