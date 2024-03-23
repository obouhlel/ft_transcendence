from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import FriendRequest, Tournament
from django.db.models.signals import m2m_changed
import datetime
import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=FriendRequest)
def notification_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "uid_" + str(instance.receiver.id),
            {
                "type": "send_notification",
                "message": "Send",
            }
        )

@receiver(post_delete, sender=FriendRequest)
def notification_deleted(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "uid_" + str(instance.sender.id),
        {
            "type": "delete_notification",
            "message": "Accepted",
        }
    )

@receiver(m2m_changed, sender=Tournament.users.through)
def tournament_players_changed(sender, instance, action, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "tournament_" + str(instance.game.id),
        {
            "type": "tournament_players_changed",
            "message": {
                "action": "Update Player Count",
                "playerCount": instance.users.count(),
                "maxPlayerCount": instance.nb_player_to_start,
                "tournamentId": instance.id,
                "users": list(instance.users.values('id', 'avatar', 'username', 'alias'))
            },
        }
    )

@receiver(post_save, sender=Tournament)
@receiver(post_delete, sender=Tournament)
def tournament_created_or_deleted(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "tournament_" + str(instance.game.id),
        {
            "type": "tournament_created_or_deleted",
            "message": {
                "action": "Update Tournament List",
                "tournaments": [tournament.tournament_data(minimal=True) for tournament in Tournament.objects.filter(game_id=instance.game.id)]
            },
        }
    )






