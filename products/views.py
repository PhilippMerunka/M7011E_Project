from rest_framework.viewsets import ModelViewSet
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect  # Add render and redirect imports


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