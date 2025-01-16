from django.db import models
from django.conf import settings
import pyotp

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    two_fa_enabled = models.BooleanField(default=False)
    two_fa_secret = models.CharField(max_length=100, blank=True, null=True)
    
    def generate_2fa_secret(self):
        if not self.two_fa_secret:
            self.two_fa_secret = pyotp.random_base32()
            self.save()
        return self.two_fa_secret

    def verify_2fa_code(self, code):
        if not self.two_fa_secret:
            return False
        totp = pyotp.TOTP(self.two_fa_secret)
        return totp.verify(code)

    def __str__(self):
        return f"Profile of {self.user.username}"
