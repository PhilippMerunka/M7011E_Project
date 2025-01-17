from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from users.models import UserProfile
import pyotp

class UserProfileTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.profile = self.user.profile

    def test_retrieve_user_profile(self):
        response = self.client.get(f'/api/user-profiles/{self.profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.profile.id)

    def test_update_user_profile(self):
        data = {
            "phone_number": "123456789",
            "address": "123 Test Street"
        }
        response = self.client.put(f'/api/user-profiles/{self.profile.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone_number, "123456789")
        self.assertEqual(self.profile.address, "123 Test Street")

    def test_update_user_profile_invalid_user(self):
        another_user = User.objects.create_user(username='anotheruser', password='password123')
        another_profile = another_user.profile
        data = {
            "phone_number": "987654321"
        }
        response = self.client.put(f'/api/user-profiles/{another_profile.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_enable_2fa(self):
        response = self.client.get('/api/users/setup-2fa/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('secret', response.data)
        self.assertIn('qr_code', response.data)

        secret = response.data['secret']
        totp = pyotp.TOTP(secret)
        valid_code = totp.now()

        response = self.client.post('/api/users/setup-2fa/', {"code": valid_code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.two_fa_enabled)

    def test_enable_2fa_invalid_code(self):
        self.client.get('/api/users/setup-2fa/')
        invalid_code = "123456"
        response = self.client.post('/api/users/setup-2fa/', {"code": invalid_code})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.two_fa_enabled)

    def test_disable_2fa(self):
        self.profile.generate_2fa_secret()
        self.profile.two_fa_enabled = True
        self.profile.save()

        response = self.client.delete('/api/users/disable-2fa/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.two_fa_enabled)
        self.assertIsNone(self.profile.two_fa_secret)

    def test_delete_user_profile(self):
        response = self.client.delete(f'/api/user-profiles/{self.profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserProfile.objects.filter(id=self.profile.id).exists())

    def test_retrieve_user_profile_invalid_user(self):
        another_user = User.objects.create_user(username='anotheruser', password='password123')
        another_profile = another_user.profile
        response = self.client.get(f'/api/user-profiles/{another_profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_register_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        }
        response = self.client.post('/api/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().username, "newuser")

    def test_login_user_with_2fa(self):
        self.profile.generate_2fa_secret()
        self.profile.two_fa_enabled = True
        self.profile.save()

        totp = pyotp.TOTP(self.profile.two_fa_secret)
        valid_code = totp.now()

        data = {
            "username": "testuser",
            "password": "password123",
            "2fa_code": valid_code
        }
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Successfully logged in", response.data['message'])

    def test_login_user_with_2fa_invalid_code(self):
        self.profile.generate_2fa_secret()
        self.profile.two_fa_enabled = True
        self.profile.save()

        invalid_code = "123456"
        data = {
            "username": "testuser",
            "password": "password123",
            "2fa_code": invalid_code
        }
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Invalid 2FA code", response.data['error'])
