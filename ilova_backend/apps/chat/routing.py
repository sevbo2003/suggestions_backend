from django.urls import path
from . import consumers
from apps.notification.consumers import NotificationConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:chat_id>/', consumers.ChatConsumer.as_asgi()),
    path('ws/notification/', NotificationConsumer.as_asgi()),
]
