from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemViewSet

urlpatterns = [
    # Cart Endpoints
    path('create/', CartViewSet.as_view({'post': 'create'}), name='cart_create'),
    path('retrieve/<int:pk>/', CartViewSet.as_view({'get': 'retrieve'}), name='cart_retrieve'),
    path('update/<int:pk>/', CartViewSet.as_view({'put': 'update'}), name='cart_update'),
    path('delete/<int:pk>/', CartViewSet.as_view({'delete': 'destroy'}), name='cart_delete'),

    # CartItem Endpoints
    path('items/create/', CartItemViewSet.as_view({'post': 'create'}), name='cart_item_create'),
    path('items/retrieve/<int:pk>/', CartItemViewSet.as_view({'get': 'retrieve'}), name='cart_item_retrieve'),
    path('items/update/<int:pk>/', CartItemViewSet.as_view({'put': 'update'}), name='cart_item_update'),
    path('items/delete/<int:pk>/', CartItemViewSet.as_view({'delete': 'destroy'}), name='cart_item_delete'),
]