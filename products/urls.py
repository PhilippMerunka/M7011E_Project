from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, product_overview
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', views.product_overview, name='products'),
]