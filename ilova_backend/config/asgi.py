import os
import django

django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

from .middlewares import JWTAuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application

from apps.chat.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})