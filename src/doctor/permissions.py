from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # Usuario autenticado + pertenece al grupo ADMIN
        return user and user.is_authenticated and user.groups.filter(name='ADMIN').exists()