from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Restrict orders to the authenticated user
        return Order.objects.filter(user=self.request.user)

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
        # Retrieve an order
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
    
class OrderItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        # Restrict order items to those in the authenticated user's orders
        return OrderItem.objects.filter(order__user=self.request.user)

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
