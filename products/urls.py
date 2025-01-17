from django.urls import path, include
from .views import ProductViewSet, ProductOverviewPageView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # Frontend pages
    path('', ProductOverviewPageView.as_view(), name='product_overview')
]
