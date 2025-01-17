from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer, UserRegistrationSerializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import UserProfile
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserProfileSerializer, UserRegistrationSerializer
from django.views.generic import TemplateView
from .permissions import IsSuperuser, IsSuperuserOrReadOnly
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

import logging
import pyotp
import qrcode
import base64
from io import BytesIO
logger = logging.getLogger(__name__)

# General User Profile views, CRUD
class UserProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsSuperuserOrReadOnly]
    
    # Filter and search capabilities
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'phone_number', 'address']  # Filterable fields
    search_fields = ['user__username', 'user__email', 'phone_number', 'address']  # Searchable fields
    ordering_fields = ['user__username', 'user__email']  # Sortable fields
    ordering = ['user__username']  # Default ordering

    def list(self, request):
        if request.user.is_superuser:
            profiles = UserProfile.objects.all()  # Superusers see all profiles
        else:
            profiles = UserProfile.objects.filter(user=request.user)  # Regular users only see their own profile
        
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        profile = get_object_or_404(UserProfile, pk=pk, user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def update(self, request, pk=None):
        profile = get_object_or_404(UserProfile, pk=pk, user=request.user)
        serializer = UserProfileSerializer(instance=profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        profile = get_object_or_404(UserProfile, pk=pk, user=request.user)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Registration API
class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Login API
class LoginAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Access the authenticated user
        user = request.user
        
        if user.profile.two_fa_enabled:
            two_fa_code = request.data.get('2fa_code')
            if not two_fa_code:
                return Response({'error': '2FA code required'}, status=400)
        
            if not user.profile.verify_2fa_code(two_fa_code):
                return Response({'error': 'Invalid 2FA code'}, status=401)
        
        logger.info(f"User {user.username} logged in successfully.")
        
        
        # Perform any additional login actions (if needed)
        return Response({
            "message": f"Successfully logged in as {user.username}",
            "username": user.username,
            "email": user.email,
            'two_fa_enabled': user.profile.two_fa_enabled
        }, status=200)

# 2FA Enable API
class Setup2FAAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve 2FA secret and QR code."""
        user_profile = request.user.profile
        secret = user_profile.generate_2fa_secret()

        # Generate QR Code
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(request.user.email, issuer_name="MyApp")
        qr = qrcode.make(uri)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_image_base64 = base64.b64encode(buffer.getvalue()).decode()

        return Response({
            "secret": secret,
            "qr_code": qr_image_base64
        }, status=200)

    def post(self, request):
        """Verify and enable 2FA."""
        code = request.data.get("code")
        user_profile = request.user.profile

        if user_profile.verify_2fa_code(code):
            user_profile.two_fa_enabled = True
            user_profile.save()
            return Response({"message": "2FA setup successful"}, status=200)
        return Response({"error": "Invalid code"}, status=400)

# 2FA Disable API
class Disable2FAAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """Disable 2FA."""
        user_profile = request.user.profile
        user_profile.two_fa_enabled = False
        user_profile.two_fa_secret = None
        user_profile.save()
        return Response({"message": "2FA disabled successfully"}, status=200)
    
class LoginPageView(TemplateView):
    template_name = 'users/login.html'

class RegisterPageView(TemplateView):
    template_name = 'users/register.html'

class Setup2FAView(TemplateView):
    template_name = 'users/setup_2fa.html'

class Verify2FAView(TemplateView):
    template_name = 'users/verify_2fa.html'
    
class UserManagementAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSuperuser]

    def post(self, request):
        """
        Promote or demote a user.
        Request Body Example:
        {
            "user_id": 2,
            "is_staff": true,
            "is_superuser": false
        }
        """
        user_id = request.data.get('user_id')
        is_staff = request.data.get('is_staff', False)
        is_superuser = request.data.get('is_superuser', False)

        try:
            user = User.objects.get(id=user_id)
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()

            return Response({
                "message": "User updated successfully",
                "user_id": user.id,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)