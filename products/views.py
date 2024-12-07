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
    products = Product.objects.all()  # Fetch all products
    return render(request, 'products/products.html', {'products': products})