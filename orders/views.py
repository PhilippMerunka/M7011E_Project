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

@login_required
def create_order(request):
    if request.method == 'POST':
        cart = request.user.cart
        if not cart.items.exists():
            return JsonResponse({'error': 'Your cart is empty'}, status=400)
        
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
        return JsonResponse({'message': 'Order created successfully', 'order_id': order.id})

@login_required
def read_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)
        items = [{'product': item.product.name, 'quantity': item.quantity, 'price': item.price} for item in order_items]
        return JsonResponse({'order_id': order.id, 'total': order.total, 'items': items})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

@login_required
def update_order(request, order_id):
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            order_items = OrderItem.objects.filter(order=order)
            order_items.delete()
            
            cart = request.user.cart
            if not cart.items.exists():
                return JsonResponse({'error': 'Your cart is empty'}, status=400)
            
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
            return JsonResponse({'message': 'Order updated successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

@login_required
def delete_order(request, order_id):
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            order.delete()
            return JsonResponse({'message': 'Order deleted successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
