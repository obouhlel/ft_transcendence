from django.urls import re_path

from . import consumers
from . import consumersNotify
from . import consumersForTournament

wss_urlpatterns = [
    re_path(r"^ws/matchmaking/$", consumers.MatchmakingConsumer.as_asgi()),
    re_path(r"^ws/notify/", consumersNotify.NotificationConsumer.as_asgi()),
    re_path(r'^ws/tournament/(?P<game_id>\d+)$', consumersForTournament.TournamentConsumer.as_asgi()),
]

def add_urlpattern(pattern, consumer):
    wss_urlpatterns.append(re_path(pattern, consumer))
