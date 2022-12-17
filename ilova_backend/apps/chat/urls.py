from django.urls import path, include
from rest_framework import routers
from apps.chat.views import ChatViewSet, MessageFileViewSet

router = routers.DefaultRouter()
router.register('chats', ChatViewSet, basename='messages')
router.register('message_files', MessageFileViewSet, basename='message_files')


urlpatterns = [
    path('', include(router.urls)),
]
