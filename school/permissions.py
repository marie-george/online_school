from rest_framework import permissions

from users.models import UserRoles


class IsOwner(permissions.BasePermission):
    message = "Вы не являетесь владельцем учетной записи. Данная операция запрещена."

    def has_permission(self, request, view):
        if request.user.is_staff or request.user.role == UserRoles.MODERATOR and request.method in ['POST', 'DELETE']:
            return False
        return True


