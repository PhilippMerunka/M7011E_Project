from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsStaffOrReadOnly
from django.views.generic import TemplateView
from rest_framework.permissions import BasePermission


class CanManageOwnOrders(BasePermission):
    """
    Custom permission to allow users to manage their own orders.
    """
    def has_object_permission(self, request, view, obj):
        # Allow only if the order belongs to the user
        return obj.user == request.user

    def has_permission(self, request, view):
        # Allow authenticated users for POST, PATCH, DELETE
        if request.method in ['POST']:
            return request.user.is_authenticated
        return False

class OrderViewSet(ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = OrderSerializer
    
    # Filter and search capabilities
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'total', 'created_at']  # Filterable fields
    search_fields = ['user__username', 'user__email']  # Searchable fields
    ordering_fields = ['user__username', 'total', 'created_at']  # Sortable fields
    ordering = ['created_at']  # Default ordering

    def get_permissions(self):
        """
        Dynamically set permissions based on the action.
        """
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), CanManageOwnOrders()]  # Restrict to own orders
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def list(self, request):
        own_only = request.query_params.get('own', 'false').lower() == 'true'
        
        if own_only:
            queryset = Order.objects.filter(user=request.user)
        elif request.user.is_staff:
            queryset = Order.objects.all()
        else:
            queryset = Order.objects.filter(user=request.user)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # Create an order from the user's cart
        cart = request.user.cart
        if not cart.items.exists():
            return Response({'error': 'Your cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(item.product.price * item.quantity for item in cart.items.all())
        order = Order.objects.create(user=request.user, total=total)

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.items.all().delete()

        return Response(self.get_serializer(order).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        Allow staff to retrieve any order.
        Regular users can only retrieve their own orders.
        """
        if request.user.is_staff:
            # Staff can retrieve any order
            order = get_object_or_404(Order, pk=pk)
        else:
            # Restrict to the user's own orders
            order = get_object_or_404(Order, pk=pk, user=request.user)

        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # Update an order by refreshing from the cart
        order = get_object_or_404(Order, pk=pk, user=request.user)
        OrderItem.objects.filter(order=order).delete()

        cart = request.user.cart
        if not cart.items.exists():
            return Response({'error': 'Your cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(item.product.price * item.quantity for item in cart.items.all())
        order.total = total
        order.save()

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.items.all().delete()

        return Response({'message': 'Order updated successfully'})

    def destroy(self, request, pk=None):
        # Delete an order
        order = get_object_or_404(Order, pk=pk, user=request.user)
        order.delete()
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class CanManageOwnOrderItems(BasePermission):
    """
    Custom permission to allow users to manage their own order items.
    """
    def has_object_permission(self, request, view, obj):
        # Allow only if the order item belongs to the user's order
        return obj.order.user == request.user

    def has_permission(self, request, view):
        # Allow authenticated users for POST, PATCH, DELETE
        if request.method in ['POST']:
            return request.user.is_authenticated
        return False

class OrderItemViewSet(ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = OrderItemSerializer
    
    # Filter and search capabilities
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['order', 'product', 'quantity', 'price']  # Filterable fields
    search_fields = ['order__user__username', 'order__user__email', 'product__name']  # Searchable fields
    ordering_fields = ['order__user__username', 'product__name', 'quantity', 'price']  # Sortable fields
    ordering = ['order__created_at']  # Default ordering

    def get_permissions(self):
        """
        Dynamically set permissions based on the action.
        """
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), CanManageOwnOrderItems()]  # Restrict to own order items
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def get_queryset(self):
        # Return all order items
        return OrderItem.objects.all()
    
    def list(self, request):
        own_only = request.query_params.get('own', 'false').lower() == 'true'
        order_id = request.query_params.get('order')
        
        queryset = self.get_queryset()
        if order_id:
            queryset = queryset.filter(order=order_id)
        elif own_only:
            queryset = queryset.filter(order__user=request.user)
        elif request.user.is_staff:
            queryset = OrderItem.objects.all()
        
        print(f"Filtered Queryset: {queryset}")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # Create a new order item (requires a valid order ID)
        order_id = request.data.get('order')
        order = get_object_or_404(Order, id=order_id, user=request.user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(order=order, price=serializer.validated_data['product'].price)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        # Retrieve a specific order item
        order_item = get_object_or_404(OrderItem, pk=pk, order__user=request.user)
        serializer = self.get_serializer(order_item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # Update an existing order item
        order_item = get_object_or_404(OrderItem, pk=pk, order__user=request.user)

        serializer = self.get_serializer(order_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        # Delete an order item
        order_item = get_object_or_404(OrderItem, pk=pk, order__user=request.user)
        order_item.delete()
        return Response({'message': 'Order item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class OrderOverviewPageView(TemplateView):
    template_name = 'orders/orders.html'
    
class OrderConfirmationPageView(TemplateView):
    template_name = 'orders/order_confirmation.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = kwargs.get('order_id')  # Get the order ID from the URL
        order = get_object_or_404(Order, id=order_id, user=self.request.user)  # Ensure the order belongs to the user
        context['order'] = order
        return context
