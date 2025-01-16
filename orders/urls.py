from django.urls import path
from .views import place_order, view_orders

urlpatterns = [
    path('place-order/', place_order, name='place_order'),
    path('view-orders/', view_orders, name='view_orders'),
]