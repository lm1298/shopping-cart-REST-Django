from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from cart.service import Cart
from .serializers import ProductSerializer, UserSerializer, ProductDetailSerializer
from .models import Product
from django.contrib.auth.models import User
from rest_framework import viewsets

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
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        cart = Cart(request)
        return Response({
            "data": list(cart.__iter__()), 
            "cart_total_price": cart.get_total_price()
        }, status=status.HTTP_200_OK)

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
                override_quantity=product.get("override_quantity", False)
            )

        return Response({"message": "cart updated"}, status=status.HTTP_202_ACCEPTED)

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})