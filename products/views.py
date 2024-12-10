from rest_framework.viewsets import ModelViewSet
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect  # Add render and redirect imports
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@login_required(login_url='/users/login/')
def product_overview(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    products = Product.objects.all()
    all_categories = Category.objects.all()

    # Filtering by category
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(categories__id=category_filter)
    
    # Sorting
    sort = request.GET.get('sort')
    order = request.GET.get('order', 'asc')
    if sort in ['name', 'price']:
        sort_key = sort if order == 'asc' else f'-{sort}'
        products = products.order_by(sort_key)
    
    return render(request, 'products/products.html', {
        'products': products,
        'all_categories': all_categories,
    })

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/users/login/')
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_ids = request.POST.getlist('categories')

        if not name or not price:
            messages.error(request, 'Name and price are required fields.')
        else:
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
            )
            product.categories.set(Category.objects.filter(id__in=category_ids))
            product.save()
            messages.success(request, f'Product "{name}" added successfully!')
            return redirect('products')

    categories = Category.objects.all()
    return render(request, 'products/add_product.html', {'categories': categories})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/users/login/')
def update_product(request, product_id):
    product = Product.objects.get(id=product_id)
        
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_ids = request.POST.getlist('categories')

        if not name or not price:
            messages.error(request, 'Name and price are required fields.')
        else:
            product.name = name
            product.description = description
            product.price = price
            product.categories.set(Category.objects.filter(id__in=category_ids))
            product.save()
            messages.success(request, f'Product "{name}" updated successfully!')
            return redirect('products')

    categories = Category.objects.all()
    return render(request, 'products/update_product.html', {
        'product': product,
        'categories': categories,
    })

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/users/login/')
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
        
    if request.method == 'POST':
        product.delete()
        messages.success(request, f'Product "{product.name}" deleted successfully!')
        return redirect('products')
        
    return render(request, 'products/delete_product.html', {'product': product})

@api_view(['GET'])
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    serializer = ProductSerializer(product)
    return Response(serializer.data)