# products/urls.py
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, add_product, product_overview
from django.urls import path, include

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', product_overview, name='products'),
    path('', include(router.urls)),  # Include router URLs
    path('add_product/', add_product, name='add_product'),
]
