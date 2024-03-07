from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import FriendRequest

@receiver(post_save, sender=FriendRequest)
def notification_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "uid_" + str(instance.receiver.id),
            {
                "type": "send_notification",
                "message": instance.friend_request_data()['message'],
            }
        )
