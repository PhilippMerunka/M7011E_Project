from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, LoginPageView, RegisterPageView, Setup2FAView, Verify2FAView
from . import views

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.LoginPageView.as_view(), name='login_page'),
    path('register/', views.RegisterPageView.as_view(), name='register_page'),
    path('setup-2fa/', views.Setup2FAView.as_view(), name='setup_2fa_page'),
    path('verify-2fa/', views.Verify2FAView.as_view(), name='verify_2fa_page'),
] + router.urls