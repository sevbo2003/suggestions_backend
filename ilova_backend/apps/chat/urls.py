from django.urls import path, include
from rest_framework import routers
from apps.chat.views import ChatViewSet

router = routers.DefaultRouter()
router.register(r'chats', ChatViewSet, basename='messages')


urlpatterns = [
    path('', include(router.urls)),
]
