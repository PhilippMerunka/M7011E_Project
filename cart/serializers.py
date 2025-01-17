from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'username', 'created_at', 'items', 'total_items', 'total_price']
        read_only_fields = ['user', 'username']
