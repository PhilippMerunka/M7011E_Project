from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Default quantity is 1 if not provided
    if quantity < 1:
        return render(request, 'cart/cart.html', {'cart': Cart.objects.get(user=request.user), 'error': 'Quantity must be at least 1'})

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity  # Increment the existing quantity
    cart_item.save()

    return render(request, 'cart/cart.html', {'cart': cart})

@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart})