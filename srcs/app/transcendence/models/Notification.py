from typing import Any
from django.utils.translation import gettext as _
from django.db import models


#----------notifications
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Notification(models.Model):
	id = models.AutoField(primary_key=True)
	message = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	is_read = models.BooleanField(default=False)
	user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
	def __str__(self):
		return str(self.id)
	def send_notification(self):
		self.is_read = False
		self.save()
	def notification_data(self):
		return {
			'id': self.id,
			'message': self.message,
			'created_at': self.created_at,
			'is_read': self.is_read,
			'user': self.user.id
	}
	def send_to_all(self, message: str):
		channel_layer = get_channel_layer()
		async_to_sync(channel_layer.group_send)(
			"public_room",
			{
				"type": "send_notification",
				"message": message
			}
		)
