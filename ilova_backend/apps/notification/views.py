from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from apps.notification.models import Notification
from apps.notification.serializers import NotificationSerializer


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(mahalla__mahalla=self.request.user.mahalla)
