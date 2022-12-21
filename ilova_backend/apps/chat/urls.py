from django.urls import path, include
from rest_framework import routers
from apps.chat.views import ChatViewSet, MessageFileViewSet, MessageIsReadView

router = routers.DefaultRouter()
router.register('chats', ChatViewSet, basename='messages')
router.register('message_files', MessageFileViewSet, basename='message_files')
router.register('message_is_read', MessageIsReadView, basename='message_is_read')


urlpatterns = [
    path('', include(router.urls)),
]
