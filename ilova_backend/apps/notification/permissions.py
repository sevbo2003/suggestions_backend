from rest_framework.permissions import BasePermission


class IsNotificationOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False
        
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user