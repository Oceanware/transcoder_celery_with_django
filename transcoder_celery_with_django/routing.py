from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from vid.consumers import VideoConsumer

ws_urlpatterns = [
    path("video_notifier/<id>/", VideoConsumer.as_asgi()),
]

