from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from .models import UserProfile
import pyotp

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.profile = UserProfile.objects.get(user=self.user)

    def test_user_profile_created(self):
        """Test that a UserProfile is automatically created when a User is created."""
        self.assertIsNotNone(self.profile)
        self.assertEqual(self.profile.user, self.user)

    def test_generate_otp(self):
        """Test OTP generation for a user profile."""
        otp_secret = self.profile.generate_otp()
        self.assertIsNotNone(otp_secret)
        self.assertEqual(len(otp_secret), 32)  # pyotp generates 32-character secrets

    def test_verify_otp(self):
        """Test OTP verification for a user profile."""
        otp_secret = self.profile.generate_otp()
        totp = pyotp.TOTP(otp_secret)
        otp = totp.now()
        self.assertTrue(self.profile.verify_otp(otp))

    def test_invalid_otp(self):
        """Test verification fails with an invalid OTP."""
        self.profile.generate_otp()
        self.assertFalse(self.profile.verify_otp('123456'))


class UserAuthenticationViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.profile = UserProfile.objects.get(user=self.user)

    def test_register_user(self):
        """Test user registration view."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_user(self):
        """Test user login view."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_login_user_with_2fa(self):
        """Test login view with 2FA enabled."""
        self.profile.generate_otp()
        self.profile.two_fa_enabled = True
        self.profile.save()

        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('verify_2fa'))

    def test_setup_2fa(self):
        """Test setup 2FA view."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('setup_2fa'), {
            'otp': pyotp.TOTP(self.profile.generate_otp()).now()
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('products'))
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.two_fa_enabled)

    def test_verify_2fa(self):
        """Test verify 2FA view."""
        otp_secret = self.profile.generate_otp()
        self.profile.two_fa_enabled = True
        self.profile.save()

        self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        response = self.client.post(reverse('verify_2fa'), {
            'otp': pyotp.TOTP(otp_secret).now()
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('products'))

    def test_logout_user(self):
        """Test logout view."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, settings.LOGOUT_REDIRECT_URL)
        self.assertNotIn('_auth_user_id', self.client.session)