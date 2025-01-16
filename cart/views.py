from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

class CartViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        # Restrict carts to the authenticated user
        return Cart.objects.filter(user=self.request.user)

    def create(self, request):
        # Prevent creating multiple carts for the same user
        if Cart.objects.filter(user=request.user).exists():
            return Response({'error': 'Cart already exists for this user'}, status=status.HTTP_400_BAD_REQUEST)

        # Automatically link the cart to the authenticated user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        # Ensure the cart belongs to the authenticated user
        cart = get_object_or_404(Cart, pk=pk, user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # Ensure the cart belongs to the authenticated user
        cart = get_object_or_404(Cart, pk=pk, user=request.user)
        serializer = self.get_serializer(cart, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        # Ensure the cart belongs to the authenticated user
        cart = get_object_or_404(Cart, pk=pk, user=request.user)
        cart.delete()
        return Response({'message': 'Cart deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class CartItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        # Restrict access to cart items in the authenticated user's cart
        return CartItem.objects.filter(cart__user=self.request.user)

    def create(self, request):
        # Ensure the cart belongs to the authenticated user
        cart = get_object_or_404(Cart, user=request.user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

        return Response(self.get_serializer(cart_item).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        # Ensure the cart item belongs to the authenticated user's cart
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # Ensure the cart item belongs to the authenticated user's cart
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        serializer = self.get_serializer(cart_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        # Ensure the cart item belongs to the authenticated user's cart
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        cart_item.delete()
        return Response({'message': 'Cart item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class CartOverviewPageView(TemplateView):
    template_name = 'cart/cart.html'