from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsOwberOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.from_problem_user.user == request.user