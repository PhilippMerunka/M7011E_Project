from django.core.exceptions import ValidationError
from django.test import TestCase
from products.models import Product, Category
from rest_framework import status
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.viewsets import ModelViewSet

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Smartphone",
            description="A high-quality smartphone",
            price=699.99,
        )
        self.product.categories.add(self.category)

    def test_product_creation_without_categories(self):
        """Test creating a product without categories"""
        product = Product.objects.create(
            name="Headphones",
            description="Noise-cancelling headphones",
            price=199.99,
        )
        self.assertEqual(product.categories.count(), 0)

    def test_invalid_product_creation(self):
        """Test creating a product with invalid fields"""
        with self.assertRaises(ValidationError):
            Product.objects.create(name="", price=-10.0).full_clean()

    def test_product_update(self):
        """Test updating a product"""
        self.product.name = "Updated Smartphone"
        self.product.save()
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.name, "Updated Smartphone")

    def test_product_deletion(self):
        """Test deleting a product"""
        product_id = self.product.id
        self.product.delete()
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=product_id)

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Smartphone",
            description="A high-quality smartphone",
            price=699.99,
        )
        self.product.categories.add(self.category)

    def test_get_products(self):
        """Test retrieving all products"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        """Test creating a new product"""
        data = {
            "name": "Headphones",
            "description": "Noise-cancelling headphones",
            "price": 199.99,
            "categories": [self.category.id],
        }
        response = self.client.post('/api/products/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_update_product(self):
        """Test updating an existing product"""
        data = {"name": "Updated Smartphone"}
        response = self.client.patch(
            f'/api/products/{self.product.id}/',
            data,
            content_type='application/json',  # Specify content type
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Smartphone")


    def test_delete_product(self):
        """Test deleting a product"""
        response = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_get_single_product(self):
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_get_nonexistent_product(self):
        response = self.client.get('/api/products/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_create_product_missing_fields(self):
        data = {"name": ""}
        response = self.client.post('/api/products/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_nonexistent_product(self):
        data = {"name": "Nonexistent Product"}
        response = self.client.patch('/api/products/9999/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product_with_categories(self):
        data = {
            "name": "Laptop",
            "description": "High-performance laptop",
            "price": 1200.00,
            "categories": [self.category.id],
        }
        response = self.client.post('/api/products/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(name="Laptop")
        self.assertIn(self.category, product.categories.all())

    def test_create_product_with_invalid_categories(self):
        data = {
            "name": "Tablet",
            "description": "Touchscreen tablet",
            "price": 500.00,
            "categories": [9999],  # Nonexistent category ID
        }
        response = self.client.post('/api/products/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer