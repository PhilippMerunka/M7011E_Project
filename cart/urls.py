from django.urls import path, include
from .views import CartOverviewPageView
from rest_framework.routers import DefaultRouter
from .views import CartViewSet

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    # Frontend page view for cart
    path('', CartOverviewPageView.as_view(), name='cart_overview_page'),
] + router.urls