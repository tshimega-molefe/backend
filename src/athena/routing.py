from django.urls import path
from emergency.consumers import EmergencyConsumer

websocket_urlpatterns = [
    path("", EmergencyConsumer.as_asgi())
]