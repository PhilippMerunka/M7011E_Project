from django.urls import path, include
from .views import OrderViewSet, OrderOverviewPageView, OrderConfirmationPageView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', OrderOverviewPageView.as_view(), name='orders'),
    path('confirmation/<int:order_id>/', OrderConfirmationPageView.as_view(), name='order_confirmation'),
]