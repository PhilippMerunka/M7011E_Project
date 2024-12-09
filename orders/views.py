from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem

@login_required
def place_order(request):
    cart = request.user.cart
    if not cart.items.exists():
        return render(request, 'orders/order_confirmation.html', {'error': 'Your cart is empty'})
        
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
    return render(request, 'orders/order_confirmation.html', {'order': order})

@login_required
def view_orders(request):
    orders = request.user.orders.all()
    return render(request, 'orders/orders.html', {'orders': orders})
