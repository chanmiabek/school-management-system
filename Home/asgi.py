import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import school.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Home.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            school.routing.websocket_urlpatterns
        )
    ),
})
