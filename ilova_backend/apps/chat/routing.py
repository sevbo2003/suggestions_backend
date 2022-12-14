from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/<str:problem_id>/', consumers.ChatConsumer.as_asgi()),
]
