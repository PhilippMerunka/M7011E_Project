from django.urls import path
from .views import place_order, view_orders

urlpatterns = [
    path('place/', place_order, name='place_order'),
    path('', view_orders, name='view_orders'),
]