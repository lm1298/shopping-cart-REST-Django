import uuid
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from cart.service import Cart
from .serializers import CartDetailSerializer, CartItemSerializer, ProductSerializer, UserSerializer, ProductDetailSerializer, RegistrationSerializer
from .models import Product
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions

from cart import serializers

class RegistrationAPIView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer

    def post(self, request):
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
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductAPI(APIView):
    """
    Single API to handle product operations
    """
    serializer_class = ProductSerializer

    def get(self, request, format=None):
        qs = Product.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    API to handle individual product operations (GET, PUT, DELETE)
    """
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminUser]  # Ensures only admin users can access

    def get_queryset(self):
        return Product.objects.all()

    # Add delete functionality
    def perform_destroy(self, instance):
        instance.delete()

class CartAPI(APIView):
    """
    Single API to handle cart operations
    """
    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {"data": list(cart.__iter__()), 
            "cart_total_price": cart.get_total_price()},
            status=status.HTTP_200_OK
            )

    def post(self, request, **kwargs):
        cart = Cart(request)

        if "remove" in request.data:
            product = request.data["product"]
            cart.remove(product)

        elif "clear" in request.data:
            cart.clear()

        else:
            product = request.data
            cart.add(
                    product=product["product"],
                    quantity=product["quantity"],
                    overide_quantity=product["overide_quantity"] if "overide_quantity" in product else False
                )

        return Response(
            {"message": "cart updated"},
            status=status.HTTP_202_ACCEPTED)
    
class CartDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    API to handle individual cart operations (GET, PUT, DELETE)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartDetailSerializer
    def get(self, request, pk=None, format=None):
        cart = Cart(request)
        serializer = CartDetailSerializer({
            "items": cart.cart_items(),
            "cart_total_price": cart.get_total_price()
        })
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, pk=None, format=None):
        cart = Cart(request)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart.update(
            product=serializer.validated_data["product"],
            quantity=serializer.validated_data["quantity"],
            override_quantity=serializer.validated_data["override_quantity"]
        )

        return Response({"message": "cart updated"}, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        cart = Cart(request)
        product_id = request.data.get("product", None)
        if product_id is not None:
            cart.remove(product_id)
            return Response({"message": "item removed from cart"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "product not specified"}, status=status.HTTP_400_BAD_REQUEST)

    
    
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})