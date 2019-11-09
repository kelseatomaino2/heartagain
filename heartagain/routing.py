from django.urls import re_path

from sensor import consumers

websocket_urlpatterns = [
    re_path(r'sensor/', consumers.EventConsumer),
]