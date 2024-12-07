from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, register_user, login_user, logout_user
from . import views
from django.shortcuts import render, redirect  # Add render and redirect imports


router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('api/', include(router.urls)),  # API endpoints
    path('register/', register_user, name='register'),  # HTML registration
    path('login/', login_user, name='login'),  # HTML login
    path('logout/', logout_user, name='logout'),
]