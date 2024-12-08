from django.shortcuts import render, redirect  # Add render and redirect imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework.viewsets import ModelViewSet
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

# HTML Views for user authentication
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Debugging: Log the received data
        print(f"Username: {username}, Email: {email}, Password: {password}")

        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'users/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            try:
                # Create the new user
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Registration successful!')

                # Render email content from template
                try:
                    # Render email content from template
                    email_content = render_to_string('emails/welcome_email.html', {'username': username})
                    email_message = EmailMessage(
                        'Welcome to MyApp!',
                        email_content,
                        settings.EMAIL_FROM_USER,
                        [email],
                    )
                    email_message.content_subtype = 'html'
                    email_message.send()
                except Exception as e:
                    print(f"Email Error: {e}")
                    messages.warning(request, 'Registration successful, but we could not send the welcome email.')


                return redirect('login')
            except Exception as e:
                # Log the exception for debugging
                print(f"Error: {e}")
                messages.error(request, 'An error occurred during registration. Please try again.')
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