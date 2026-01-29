import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import notifications.routing  # import your notifications app routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backendproject.settings")

# This is for normal HTTP requests
django_asgi_app = get_asgi_application()

# ASGI application for Channels
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # existing HTTP support
    "websocket": AuthMiddlewareStack(
        URLRouter(
            notifications.routing.websocket_urlpatterns
        )
    ),
})