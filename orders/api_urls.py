from django.urls import path
from .views import OrderViewSet, OrderItemViewSet

urlpatterns = [
    # Order CRUD Endpoints
    path('create/', OrderViewSet.as_view({'post': 'create'}), name='order_create'),
    path('retrieve/<int:pk>/', OrderViewSet.as_view({'get': 'retrieve'}), name='order_retrieve'),
    path('update/<int:pk>/', OrderViewSet.as_view({'put': 'update'}), name='order_update'),
    path('delete/<int:pk>/', OrderViewSet.as_view({'delete': 'destroy'}), name='order_delete'),

    # Order Item CRUD Endpoints
    path('items/create/', OrderItemViewSet.as_view({'post': 'create'}), name='order_item_create'),
    path('items/retrieve/<int:pk>/', OrderItemViewSet.as_view({'get': 'retrieve'}), name='order_item_retrieve'),
    path('items/update/<int:pk>/', OrderItemViewSet.as_view({'put': 'update'}), name='order_item_update'),
    path('items/delete/<int:pk>/', OrderItemViewSet.as_view({'delete': 'destroy'}), name='order_item_delete'),
]
