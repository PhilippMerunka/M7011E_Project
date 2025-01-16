from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, UserRegistrationAPIView, LoginAPIView, Setup2FAAPIView, Disable2FAAPIView

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('setup-2fa/', Setup2FAAPIView.as_view(), name='setup_2fa'),
    path('disable-2fa/', Disable2FAAPIView.as_view(), name='disable_2fa'),
] + router.urls