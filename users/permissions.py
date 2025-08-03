from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Право владельца"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModerator(BasePermission):
    """Право модератора"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderators").exists()
