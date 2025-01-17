import unittest
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product

# FILE: cart/test_tests.py


class CartViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.cart_url = reverse('cart-list')

    def test_create_cart(self):
        response = self.client.post(self.cart_url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.get().user, self.user)

    def test_create_cart_already_exists(self):
        Cart.objects.create(user=self.user)
        response = self.client.post(self.cart_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Cart.objects.count(), 1)

    def test_retrieve_cart(self):
        cart = Cart.objects.create(user=self.user)
        url = reverse('cart-detail', args=[cart.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CartSerializer(cart).data)

    def test_create_cart_unauthenticated(self):
        self.client.logout()  # Desconecta al usuario
        response = self.client.post(self.cart_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  


    def test_list_carts_as_admin(self):
        admin = User.objects.create_superuser(username='admin', password='adminpass')
        self.client.force_authenticate(user=admin)
        Cart.objects.create(user=self.user)
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Cart.objects.count())

    def test_retrieve_own_cart(self):
        cart = Cart.objects.create(user=self.user)
        url = reverse('cart-detail', args=[cart.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], cart.id)

    def test_retrieve_other_user_cart(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        other_cart = Cart.objects.create(user=other_user)
        url = reverse('cart-detail', args=[other_cart.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_carts(self):
        Cart.objects.create(user=self.user)
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Cart.objects.count())

class CartItemViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item_url = reverse('cart-item-list') 

    def test_create_cart_item(self):
        product = Product.objects.create(name='Test Product', price=10.0)
        data = {'cart': self.cart.id, 'product': product.id, 'quantity': 2}  
        response = self.client.post(self.cart_item_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.get().product, product)

    def test_update_cart_item(self):
        product = Product.objects.create(name='Test Product', price=10.0)
        cart_item = CartItem.objects.create(cart=self.cart, product=product, quantity=1)
        url = reverse('cart-item-detail', args=[cart_item.id])
        data = {'quantity': 3}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)  
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 3)

    def test_destroy_cart_item(self):
        product = Product.objects.create(name='Test Product', price=10.0)
        cart_item = CartItem.objects.create(cart=self.cart, product=product, quantity=1)
        url = reverse('cart-item-detail', args=[cart_item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_create_cart_item_invalid_quantity(self):
        product = Product.objects.create(name='Invalid Product', price=5.0)
        data = {'cart': self.cart.id, 'product': product.id, 'quantity': -1}
        response = self.client.post(self.cart_item_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('quantity', response.data)

    def test_update_other_user_cart_item(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        other_cart = Cart.objects.create(user=other_user)
        product = Product.objects.create(name='Other Product', price=10.0)
        cart_item = CartItem.objects.create(cart=other_cart, product=product, quantity=1)
        url = reverse('cart-item-detail', args=[cart_item.id])
        data = {'quantity': 5}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_cart_item(self):
        product = Product.objects.create(name='Test Product', price=10.0)
        cart_item = CartItem.objects.create(cart=self.cart, product=product, quantity=1)
        url = reverse('cart-item-detail', args=[cart_item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], cart_item.id)

    def test_list_cart_items(self):
        product1 = Product.objects.create(name='Product 1', price=10.0)
        product2 = Product.objects.create(name='Product 2', price=20.0)
        CartItem.objects.create(cart=self.cart, product=product1, quantity=1)
        CartItem.objects.create(cart=self.cart, product=product2, quantity=2)
        response = self.client.get(self.cart_item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_cart_items_as_admin(self):
        admin = User.objects.create_superuser(username='admin', password='adminpass')
        self.client.force_authenticate(user=admin)
        product = Product.objects.create(name='Test Product', price=10.0)
        CartItem.objects.create(cart=self.cart, product=product, quantity=1)
        response = self.client.get(self.cart_item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_cart_item_unauthenticated(self):
        self.client.logout()
        product = Product.objects.create(name='Test Product', price=10.0)
        data = {'cart': self.cart.id, 'product': product.id, 'quantity': 2}
        response = self.client.post(self.cart_item_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

if __name__ == '__main__':
    unittest.main() 