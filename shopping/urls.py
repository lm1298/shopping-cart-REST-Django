"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cart.views import  CartAPI, ClearCartAPI, DetailUser, ListUser, ProductAPI
from django.conf import settings
from django.conf.urls.static import static

from shopping import settings
from cart import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.RegistrationAPIView.as_view(), name='register'),
    path('users/', views.ListUser.as_view(), name='users-list'),
    path('users/<int:pk>/', views.DetailUser.as_view(), name='user-detail'),
    path('productapi/', views.ProductAPI.as_view(), name='products'),
    path('products/', views.ProductAPIView.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetailAPI.as_view(), name='product-detail'),
    path('cart/', views.CartAPI.as_view(), name='cart'),
    path('cart/clear/', views.ClearCartAPI.as_view(), name='clear_cart'),
    path('', views.home, name='home'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)