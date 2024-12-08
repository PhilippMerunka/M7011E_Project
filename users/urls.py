from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, register_user, login_user, logout_user, setup_2fa, verify_2fa
from . import views
from django.shortcuts import render, redirect  # Add render and redirect imports


router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('api/', include(router.urls)),  # API endpoints
    path('register/', register_user, name='register'),  # HTML registration
    path('login/', login_user, name='login'),  # HTML login
    path('logout/', logout_user, name='logout'),
    path('setup-2fa/', views.setup_2fa, name='setup_2fa'),
    path('verify-2fa/', views.verify_2fa, name='verify_2fa'),
]