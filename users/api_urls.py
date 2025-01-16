from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet,
    UserRegistrationAPIView,
    LoginAPIView,
    Setup2FAAPIView,
    Disable2FAAPIView,
    UserManagementAPIView,
    RetrieveUserAPIView,
    UpdateUserAPIView,
    DeleteUserAPIView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    # JWT Token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User management endpoints
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    
    path('setup-2fa/', Setup2FAAPIView.as_view(), name='setup_2fa'),
    path('disable-2fa/', Disable2FAAPIView.as_view(), name='disable_2fa'),
    
    # User management for superusers
    path('manage/', UserManagementAPIView.as_view(), name='user_management'),
    path('retrieve/<int:user_id>/', RetrieveUserAPIView.as_view(), name='retrieve_user'),
    path('update/<int:user_id>/', UpdateUserAPIView.as_view(), name='update_user'),
    path('delete/<int:user_id>/', DeleteUserAPIView.as_view(), name='delete_user'),
]

# Include router-generated routes
urlpatterns += router.urls
