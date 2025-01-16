from django.urls import path
from .views import ProductViewSet, CategoryViewSet

urlpatterns = [
    # Product Endpoints
    path('create/', ProductViewSet.as_view({'post': 'create'}), name='product_create'),
    path('retrieve/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve'}), name='product_retrieve'),
    path('update/<int:pk>/', ProductViewSet.as_view({'put': 'update'}), name='product_update'),
    path('delete/<int:pk>/', ProductViewSet.as_view({'delete': 'destroy'}), name='product_delete'),

    # Category Endpoints
    path('categories/create/', CategoryViewSet.as_view({'post': 'create'}), name='category_create'),
    path('categories/retrieve/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve'}), name='category_retrieve'),
    path('categories/update/<int:pk>/', CategoryViewSet.as_view({'put': 'update'}), name='category_update'),
    path('categories/delete/<int:pk>/', CategoryViewSet.as_view({'delete': 'destroy'}), name='category_delete'),
]
