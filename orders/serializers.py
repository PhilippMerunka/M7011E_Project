from rest_framework import serializers
from .models import Order, OrderItem

class OrderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'username', 'created_at', 'total', 'items']
        read_only_fields = ['user', 'username', 'created_at', 'total', 'items']

    def get_items(self, obj):
        # Retrieve only items associated with the current order instance
        items = obj.items.all()  # Use the related_name 'items' defined in the OrderItem model
        return OrderItemSerializer(items, many=True).data
    
    def get_total(self, obj):
        return obj.total

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']
        read_only_fields = ['order', 'price']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value