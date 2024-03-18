from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import FriendRequest
from django.db.models.signals import m2m_changed
from .models import Tournament
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
    logger.info(f"###### Signal m2m_changed reçu, action : , {action}")
    logger.info(f"###### Instance.game : , {instance.game}")
    logger.info(f"###### Instance.game.id : , {instance.game.id}")
    # logger.info("Sender :", sender)
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
            },
        }
    )




