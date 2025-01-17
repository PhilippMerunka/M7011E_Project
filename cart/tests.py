from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Cart, CartItem
from products.models import Product, Category

class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_creation(self):
        self.assertEqual(self.cart.user.username, 'testuser')
        self.assertEqual(self.cart.total_items(), 0)
        self.assertEqual(self.cart.total_price(), 0)

    def test_cart_str(self):
        self.assertEqual(str(self.cart), f"Cart of {self.user.username}")

class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Smartphone", price=699.99)
        self.product.categories.add(self.category)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.cart.user.username, 'testuser')
        self.assertEqual(self.cart_item.product.name, 'Smartphone')
        self.assertEqual(self.cart_item.quantity, 2)

    def test_cart_item_str(self):
        self.assertEqual(str(self.cart_item), f"{self.cart_item.quantity} of {self.cart_item.product.name}")

class CartAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.cart = Cart.objects.create(user=self.user)

    def test_get_cart(self):
        response = self.client.get(reverse('cart-detail', kwargs={'pk': self.cart.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)

    def test_create_cart(self):
        response = self.client.post(reverse('cart-list'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 2)

    def test_update_cart(self):
        response = self.client.patch(reverse('cart-detail', kwargs={'pk': self.cart.id}), {'user': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_delete_cart(self):
        response = self.client.delete(reverse('cart-detail', kwargs={'pk': self.cart.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cart.objects.count(), 0)

class CartItemAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Smartphone", price=699.99)
        self.product.categories.add(self.category)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_get_cart_item(self):
        response = self.client.get(reverse('cartitem-detail', kwargs={'pk': self.cart_item.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product'], self.product.id)

    def test_create_cart_item(self):
        data = {'cart': self.cart.id, 'product': self.product.id, 'quantity': 1}
        response = self.client.post(reverse('cartitem-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 2)

    def test_update_cart_item(self):
        data = {'quantity': 3}
        response = self.client.patch(reverse('cartitem-detail', kwargs={'pk': self.cart_item.id}), data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 3)

    def test_delete_cart_item(self):
        response = self.client.delete(reverse('cartitem-detail', kwargs={'pk': self.cart_item.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_cart_item_total_price(self):
        self.assertEqual(self.cart_item.product.price * self.cart_item.quantity, 1399.98)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cart.objects.count(), 0)

class CartItemAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Smartphone", price=699.99)
        self.product.categories.add(self.category)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_get_cart_item(self):
        response = self.client.get(reverse('cartitem-detail', kwargs={'pk': self.cart_item.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product'], self.product.id)

    def test_create_cart_item(self):
        data = {'cart': self.cart.id, 'product': self.product.id, 'quantity': 1}
        response = self.client.post(reverse('cartitem-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 2)

    def test_update_cart_item(self):
        data = {'quantity': 3}
        response = self.client.patch(reverse('cartitem-detail', kwargs={'pk': self.cart_item.id}), data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 3)

    def test_delete_cart_item(self):
        response = self.client.delete(reverse('cartitem-detail', kwargs={'pk': self.cart_item.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)

class CartAdditionalTests(APITestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password456')

        # Create categories and products
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Smartphone", price=699.99)
        self.product.categories.add(self.category)

        # Create carts
        self.cart = Cart.objects.create(user=self.user)
        self.other_cart = Cart.objects.create(user=self.other_user)

        # Create a cart item
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

        # Authenticate the client
        self.client.login(username='testuser', password='password123')

    def test_only_owner_can_access_cart(self):
        # Attempt to access another user's cart
        response = self.client.get(f'/api/carts/{self.other_cart.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_negative_quantity_not_allowed(self):
        # Attempt to create a CartItem with negative quantity
        data = {'cart': self.cart.id, 'product': self.product.id, 'quantity': -1}
        response = self.client.post('/api/items/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_zero_quantity_not_allowed(self):
        # Attempt to create a CartItem with zero quantity
        data = {'cart': self.cart.id, 'product': self.product.id, 'quantity': 0}
        response = self.client.post('/api/items/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_product_addition(self):
        # Attempt to add a duplicate product to the cart
        data = {'cart': self.cart.id, 'product': self.product.id, 'quantity': 1}
        response = self.client.post('/api/items/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cart_empty_behavior(self):
        # Verify behavior with an empty cart
        CartItem.objects.all().delete()  # Empty the cart
        response = self.client.get(f'/api/carts/{self.cart.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_items'], 0)
        self.assertEqual(response.data['total_price'], '0.00')

    def test_unauthenticated_user_access(self):
        # Attempt to access the API without authentication
        self.client.logout()
        response = self.client.get(f'/api/carts/{self.cart.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_existent_cart_access(self):
        # Attempt to access a non-existent cart
        response = self.client.get('/api/carts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_non_existent_cart_item_access(self):
        # Attempt to access a non-existent CartItem
        response = self.client.get('/api/items/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('cart.models.Cart.total_price')
    def test_delete_cart_item_reduces_total(self, mock_total_price):
        # Mock the total price calculation for performance optimization
        mock_total_price.return_value = 0
        response = self.client.delete(f'/api/items/{self.cart_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.total_items(), 0)
        self.assertEqual(self.cart.total_price(), 0)
