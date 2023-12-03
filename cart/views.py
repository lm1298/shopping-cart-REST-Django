import uuid
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from cart.service import Cart
from .serializers import  ProductSerializer, UserSerializer, ProductDetailSerializer, RegistrationSerializer
from .models import Product
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action

from cart import serializers

class RegistrationAPIView(generics.GenericAPIView):
    """
    API view for user registration.

    Users can be registered by providing necessary information.

    References: https://github.com/propenster/youtube-django-ecommerce-api.git
    """

    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Handle POST requests for user registration.

        Args:
            request: HTTP request object.

        Returns:
            Response: JSON response containing registration status and user details.
        """
        
        serializer = self.get_serializer(data = request.data)
        # serializer.is_valid(raise_exception = True)
        # serializer.save()
        if(serializer.is_valid()):
            serializer.save()
            return Response({
                "RequestId": str(uuid.uuid4()),
                "Message": "User created successfully",
                
                "User": serializer.data}, status=status.HTTP_201_CREATED
                )
        
        return Response({"Errors": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)

class ListUser(generics.ListCreateAPIView):
    """
    API view to list and create users.

    Users can be listed and created by authenticated users.

    References: https://github.com/propenster/youtube-django-ecommerce-api.git
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, and delete user details.

    Authenticated users can retrieve, update, and delete their own details.

    References: https://github.com/propenster/youtube-django-ecommerce-api.git
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.

    Reference: https://github.com/jessanettica/simple-shopping-api.git
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductAPI(APIView):
    """
    Single API to handle product operations 

    Reference: https://dev.to/nick_langat/building-a-shopping-cart-using-django-rest-framework-54i0
    """
    serializer_class = ProductSerializer

    def get(self, request, format=None):
        """
        Handle GET requests to retrieve a list of products.

        Args:
            request: HTTP request object.
            format: Format of the requested data.

        Returns:
            Response: JSON response containing the list of products.
        """
        qs = Product.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new product.

        Args:
            request: HTTP request object.
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response containing the details of the created product.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    API to handle individual product operations (GET, PUT, DELETE)
    """
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminUser]  

    def get_queryset(self):
        return Product.objects.all()

    def perform_destroy(self, instance):
        instance.delete()

class CartAPI(APIView):
    """
    Single API to handle cart operations

    Contributors: Prasanna
    References: 
    1. https://github.com/F4R4N/shop-django-rest-framework.git
    2. https://github.com/jessanettica/simple-shopping-api.git 
    """
    def get(self, request, format=None):
        cart = Cart(request)
        return Response(
            {"data": list(cart), 
            "cart_total_price": cart.get_total_price()},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'], url_path='remove-from-cart')
    def remove_from_cart(self, request):
        """
        Handle POST requests to remove a product from the cart.

        Args:
            request: HTTP request object.

        Returns:
            Response: JSON response indicating the status of the removal operation.
        """
        cart = Cart(request)
        product_id = request.data.get("product_id")
        if product_id:
            cart.remove(product_id)
            return Response({"message": "Product removed from the cart"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='clear-cart')
    def clear_cart(self, request):
        """
        Handle POST requests to clear the entire cart.

        Args:
            request: HTTP request object.

        Returns:
            Response: JSON response indicating the status of the cart clearing operation.
        """
        cart = Cart(request)
        cart.clear()
        return Response({"message": "Cart cleared successfully"}, status=status.HTTP_200_OK)
    
    def post(self, request, **kwargs):
        """
        Handle POST requests to update the cart.

        Args:
            request: HTTP request object.
            kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response indicating the status of the cart update operation.
        """
        cart = Cart(request)

        if "remove" in request.data:
            product = request.data["product"]
            cart.remove(product)
        elif "clear" in request.data:
            cart.clear()
        else:
            product = request.data.get("product")
            cart.add(
                product=product,
                quantity=request.data.get("quantity"),
                override_quantity=request.data.get("override_quantity", False)
            )

        return Response(
            {"message": "cart updated"},
            status=status.HTTP_202_ACCEPTED
        )

    
def home(request):
    """
    Render the home page.

    Args:
        request: HTTP request object.

    Returns:
        Response: Rendered HTML page with the list of products.
    """
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})