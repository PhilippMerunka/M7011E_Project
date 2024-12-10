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
import qrcode
import io
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import pyotp
import base64
from django.contrib.auth import get_backends

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
            # Ensure the user has a profile
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)
            
            if user.profile.two_fa_enabled:
                request.session['pre_2fa_user'] = user.id
                return redirect('verify_2fa')
            login(request, user)
            return redirect('products')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'users/login.html')

def logout_user(request):
    # Check if the user logged in via Google OAuth
    is_google_user = request.user.is_authenticated and request.user.social_auth.filter(provider='google-oauth2').exists()

    # Log the user out of the Django session
    logout(request)
    request.session.pop('pre_2fa_user', None)  # Clear the session variable

    # If the user logged in via Google OAuth, redirect to Google's logout URL
    if is_google_user:
        return redirect('https://accounts.google.com/logout')

    # Otherwise, redirect to the homepage or login page
    return redirect(settings.LOGOUT_REDIRECT_URL)


@login_required
def setup_2fa(request):
    profile = request.user.profile
    secret = profile.generate_otp()

    if request.method == 'POST':
        otp = request.POST.get('otp')
        if profile.verify_otp(otp):
            profile.two_fa_enabled = True
            profile.save()
            messages.success(request, '2FA enabled successfully.')
            return redirect('products')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    # Generate QR code
    otpauth_url = pyotp.TOTP(secret).provisioning_uri(request.user.email, issuer_name="MyApp")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(otpauth_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img = img.resize((300, 300))  # Resize the QR code to 300x300 pixels
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    qr_image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return render(request, 'users/setup_2fa.html', {'qr_image_base64': qr_image_base64})

def verify_2fa(request):
    user_id = request.session.get('pre_2fa_user')
    
    if not user_id:
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid user session.')
        return redirect('login')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        if user.profile.verify_otp(otp):
            # Set the backend explicitly for OAuth logins
            backend = get_backends()[0]  # Use the first backend or appropriate one
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            login(request, user)  # Log the user in
            request.session.pop('pre_2fa_user', None)
            return redirect('products')  # Redirect to the desired page
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'users/verify_2fa.html')

@login_required
def update_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = request.user
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.set_password(password)
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'users/update_user.html')

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Account deleted successfully.')
        return redirect('register')

    return render(request, 'users/delete_user.html')

@login_required
def view_profile(request):
    profile = request.user.profile
    return render(request, 'users/view_profile.html', {'profile': profile})