from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.type == 'AdminUser':
                return True
        return False
