import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.group_name = 'public_room'
		await self.channel_layer.group_add(
			self.group_name,
			self.channel_name
		)
		logger.info("Connected to public room")
		logger.info("uid#" + str(self.scope['user'].id))
		await self.channel_layer.group_add(
			"uid_" + str(self.scope['user'].id),
			self.channel_name
		)
		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.group_name,
			self.channel_name
		)

	async def send_notification(self, event):
		await self.send(text_data=json.dumps({ 'message': event['message'] }))

	async def delete_notification(self, event):
		await self.send(text_data=json.dumps({ 'message': event['message'] }))