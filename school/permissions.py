from rest_framework import permissions

from users.models import UserRoles


class IsModerator(permissions.BasePermission):
    message = "Вы не являетесь модератором"

    def has_permission(self, request, view):
        if request.user.role == UserRoles.MODERATOR:
            return True
        return False


class IsOwner(permissions.BasePermission):
    message = "Вы не являетесь владельцем учетной записи"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False
