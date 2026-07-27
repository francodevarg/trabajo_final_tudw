from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # Usuario autenticado + pertenece al grupo ADMIN
        return user and user.is_authenticated and user.groups.filter(name='ADMIN').exists()

class IsAdminOrOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        is_admin = request.user.groups.filter(
            name="ADMIN"
        ).exists()

        is_owner = obj.user == request.user

        return is_admin or is_owner