from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, product_overview
from django.urls import path, include

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', product_overview, name='products'),
    
    path('', include(router.urls)),
]
