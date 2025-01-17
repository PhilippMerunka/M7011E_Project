from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import CategorySerializer, ProductSerializer
from users.permissions import IsStaffOrReadOnly, IsSuperuserOrReadOnly
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class ProductViewSet(ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = ProductSerializer
    
     # Filter and search capabilities
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categories', 'price']  # Filterable fields
    search_fields = ['name', 'description']  # Searchable fields
    ordering_fields = ['price', 'name']  # Sortable fields
    ordering = ['price']  # Default ordering

    def get_queryset(self):
        # Return all products
        return Product.objects.all()
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request):
        # Create a new product
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        # Retrieve a specific product
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # Update an existing product
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        # Delete a product
        product = self.get_object()
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class CategoryViewSet(ModelViewSet):
    permission_classes = [IsSuperuserOrReadOnly]
    serializer_class = CategorySerializer
    
    # Add filter and search capabilities
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']  # Filterable fields
    search_fields = ['name']  # Searchable fields
    ordering_fields = ['name']  # Sortable fields
    ordering = ['name']  # Default ordering

    def get_queryset(self):
        print("Fetching categories")
        # Return all categories
        return Category.objects.all()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request):
        # Create a new category
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        # Retrieve a specific category
        category = self.get_object()
        serializer = self.get_serializer(category)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # Update an existing category
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        # Delete a category
        category = self.get_object()
        category.delete()
        return Response({'message': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class ProductOverviewPageView(TemplateView):
    template_name = 'products/products.html'
    
def product_overview(request):
    all_categories = Category.objects.all()
    selected_category_id = request.GET.get('category', '')

    # Add a "selected" attribute to categories
    for category in all_categories:
        category.selected = "selected" if str(category.id) == str(selected_category_id) else ""

    return render(request, 'products/products.html', {
        'all_categories': all_categories,
    })