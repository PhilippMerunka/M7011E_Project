from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def recalculate_total(self):
        # Calculate total based on related OrderItems
        self.total = sum(item.price * item.quantity for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Ensure the price is correct and linked to the product's current price
        self.price = self.product.price
        super().save(*args, **kwargs)
        # Recalculate order total whenever an item is saved
        self.order.recalculate_total()

    def delete(self, *args, **kwargs):
        # Recalculate order total when an item is deleted
        super().delete(*args, **kwargs)
        self.order.recalculate_total()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order #{self.order.id}"