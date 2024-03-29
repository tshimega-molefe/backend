"""
ASGI config for athena project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from emergency.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'athena.settings')

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  "websocket":  AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
})