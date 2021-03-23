from channels.routing import URLRouter
from django.urls import path

from mpact.consumers import ConnectionConsumer

websockets = URLRouter(
    [
        path("ws/connection", ConnectionConsumer.as_asgi()),
    ]
)
