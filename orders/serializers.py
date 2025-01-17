from rest_framework import serializers
from .models import Order, OrderItem

class OrderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'username', 'created_at', 'total', 'items']
        read_only_fields = ['user', 'username', 'created_at', 'total', 'items']

    def get_items(self, obj):
        # Serialize related OrderItems
        items = OrderItem.objects.filter(order=obj)
        return OrderItemSerializer(items, many=True).data

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']
        read_only_fields = ['order', 'price']