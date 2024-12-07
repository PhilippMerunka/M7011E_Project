from django.shortcuts import render, redirect  # Add render and redirect imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework.viewsets import ModelViewSet
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

# HTML Views for user authentication
def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Registration successful!')
            return redirect('login')
    return render(request, 'users/register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('products')  # Redirect to products or another page
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'users/login.html')


def logout_user(request):
    # Check if the user logged in via Google OAuth
    is_google_user = request.user.is_authenticated and request.user.social_auth.filter(provider='google-oauth2').exists()

    # Log the user out of the Django session
    logout(request)

    # If the user logged in via Google OAuth, redirect to Google's logout URL
    if is_google_user:
        return redirect('https://accounts.google.com/logout')

    # Otherwise, redirect to the homepage or login page
    return redirect(settings.LOGOUT_REDIRECT_URL)