from django.urls import re_path
from .consumers import ChatConsumer
from polls.consumers import PollConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_uuid>[0-9a-f-]+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/poll/(?P<room_uuid>[^/]+)/$', PollConsumer.as_asgi()),
]
