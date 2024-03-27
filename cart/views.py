import requests
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from cart.service import Cart
from cart import serializers
from .serializers import CartSerializer, ProductSerializer, UserSerializer
from .serializers import ProductDetailSerializer, RegistrationSerializer
from .models import Product
from rest_framework.generics import RetrieveAPIView, DestroyAPIView
from .models import Cart


class RegistrationMixin:
    """
    A mixin providing user registration functionality.
    """
    serializer_class = RegistrationSerializer

    def register_user(self, request):
        """
        Register a user based on the provided request data.

        Args:
            request (HttpRequest): The HTTP request object containing user registration data.

        Returns:
            Response: JSON response containing the registration status and user details.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "RequestId": str(uuid.uuid4()),
                "Message": "User created successfully",
                "User": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"Errors": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)

class RegistrationAPIView(generics.GenericAPIView, RegistrationMixin):
    """
    API view for user registration.

    Users can be registered by providing necessary information.

    References: https://github.com/propenster/youtube-django-ecommerce-api.git
    """
    def post(self, request):
        """
        POST method for user registration.
        """
        return self.register_user(request)

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

    Reference: https://github.com/jessanettica/simple-shopping-api.git.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductAPI(APIView):
    """
    Single API to handle product operations
    Reference: https://dev.to/nick_langat/building-a-shopping-cart-using-django-rest-framework-54i0.
    """

    def get(self, request):
        """
        Handle GET requests to retrieve a list of products.
        """
        try:
            # Fetch products from external API
            response = requests.get('https://fakestoreapi.com/products')
            response.raise_for_status()
            external_products_data = response.json()

            # Fetch products from database
            db_products = Product.objects.all()
            db_products_data = ProductSerializer(db_products, many=True).data

            # Combine the products from the external API and the database
            all_products_data = external_products_data + db_products_data

            return Response(all_products_data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": f"Failed to fetch products: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"Error processing products: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        """
        Handle POST requests to create a new product.

        Returns:
            Response: JSON response containing the details of the created product.
        """
        serializer = ProductSerializer(data=request.data, files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ProductAPIView(APIView):
    """
    Single API to handle product operations
    """
    serializer_class = ProductSerializer

    def get(self, request, format=None):
        qs = Product.objects.all()

        return Response(
            {"data": self.serializer_class(qs, many=True).data}, 
            status=status.HTTP_200_OK
            )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
            )

class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    API to handle individual product operations (GET, DELETE)
    """
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get('pk')

        # Try to fetch the product from the database
        try:
            product = Product.objects.get(pk=product_id)
            serializer = ProductDetailSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            # If the product is not found in the database, try to fetch it from the external API
            response = requests.get(f'https://fakestoreapi.com/products/{product_id}')

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    def perform_destroy(self, instance):
        instance.delete()

class CartAPI(generics.ListCreateAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        return cart.items.all()

    def perform_create(self, serializer):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        serializer.save(cart=cart)

class ClearCartAPI(APIView):
    def post(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def home(request):
    """
    Render the home page.

    Args:
        request: HTTP request object.

    Returns:
        Response: Rendered HTML page with the list of products.
    """
    try:
        response = requests.get('https://fakestoreapi.com/products')
        response.raise_for_status()
        products = response.json()
        return render(request, 'home.html', {'products': products})
    except requests.RequestException as e:
        return render(request, 'home.html', {'error': f"Failed to fetch products: {str(e)}"})
