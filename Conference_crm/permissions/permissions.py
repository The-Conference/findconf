from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnlyOrAdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_superuser:
            return True
        return False
