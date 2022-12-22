from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.notification.views import NotificationViewSet, UserNotificationViewSet, MahallaViewSet

router = DefaultRouter()
router.register('notifications', NotificationViewSet, basename='notification')
router.register('user-notifications', UserNotificationViewSet, basename='user-notification')
router.register('mahalla', MahallaViewSet, basename='mahallalar')


urlpatterns = [
    path('', include(router.urls)),
]