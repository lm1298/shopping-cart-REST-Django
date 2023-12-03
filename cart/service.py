from decimal import Decimal

from django.conf import settings

from .serializers import ProductSerializer
from .models import Product


class Cart:
    """
    A class representing a shopping cart.

    The cart is stored in the user's session and contains information
    about the products added, their quantities, and total price.

    Methods:
    - __init__: Initialize the cart.
    - __iter__: Allow iteration over cart items.
    - save: Save the cart to the session.
    - add: Add a product to the cart or update its quantity.
    - remove: Remove a product from the cart.
    - __len__: Get the total number of items in the cart.
    - get_total_price: Get the total price of all items in the cart.
    - clear: Clear the entire cart.

    Reference:
    https://dev.to/nick_langat/building-a-shopping-cart-using-django-rest-framework-54i0
    """
    def __init__(self, request):
        """
        initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):    
        return iter(self.items)
    
    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add product to the cart or update its quantity
        """

        product_id = str(product["id"])
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product["price"])
            }
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()


    def remove(self, product):
        """
        Remove a product from the cart
        """
        product_id = str(product["id"])

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Loop through cart items and fetch the products from the database
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = ProductSerializer(product).data
        for item in cart.values():
            item["price"] = Decimal(item["price"]) 
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()