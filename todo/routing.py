# WebSocket URL routing for the todo app
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Example WebSocket route - uncomment and modify as needed
    # re_path(r'ws/todo/$', consumers.TodoConsumer.as_asgi()),
]
