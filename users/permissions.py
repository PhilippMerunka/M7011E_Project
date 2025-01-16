from rest_framework.permissions import BasePermission

class IsStaffOrReadOnly(BasePermission):
    """
    Custom permission to allow only staff users to create, update, or delete products.
    """
    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for all authenticated users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        # Allow write permissions only for staff users
        return request.user.is_staff

class IsSuperuserOrReadOnly(BasePermission):
    """
    Custom permission to allow only superusers to create, update, or delete categories.
    """
    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for all authenticated users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        # Allow write permissions only for superusers
        return request.user.is_superuser

class IsSuperuser(BasePermission):
    """
    Custom permission to allow only superusers to access a view.
    """
    def has_permission(self, request, view):
        return request.user.is_superuser