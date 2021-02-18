import os

import django
from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
# from .. import control_panel
import control_panel.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'signal_control_panel.settings')
django.setup()

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            control_panel.routing.websocket_urlpatterns
        )
    ),
})