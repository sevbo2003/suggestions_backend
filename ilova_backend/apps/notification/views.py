from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from apps.notification.models import Notification
from apps.notification.serializers import NotificationSerializer, NotificationCreateSerializer


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        mahallalar = self.request.user.mahallalar.all()
        return self.queryset.filter(mahalla__in=mahallalar)
    

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return NotificationCreateSerializer
        return super().get_serializer_class()