from django.urls import re_path

from . import consumers
from . import consumersForPong

wss_urlpatterns = [
    re_path(r"^ws/matchmaking/$", consumers.MatchmakingConsumer.as_asgi()),
    re_path(r"^ws/notify/", consumers.NotificationConsumer.as_asgi()),
]

def add_urlpattern(pattern, consumer):
    wss_urlpatterns.append(re_path(pattern, consumer))