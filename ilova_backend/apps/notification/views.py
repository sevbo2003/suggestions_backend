from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from apps.notification.models import Notification, UserNotification
from apps.notification.serializers import NotificationSerializer, NotificationCreateSerializer, UserNotificationSerializer
from apps.notification.permissions import IsNotificationOwner
from rest_framework.validators import ValidationError


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return NotificationCreateSerializer
        return super().get_serializer_class()


class UserNotificationViewSet(ModelViewSet):
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationSerializer
    permission_classes = [IsNotificationOwner]
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get_object(self):
        object = super().get_object()
        if object.user == self.request.user:
            object.is_read = True
            object.save()
            return object
        raise ValidationError({"message": "You can't access this notification"})
