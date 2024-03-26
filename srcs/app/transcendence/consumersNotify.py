import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import asyncio

class NotificationConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.channel_layer.group_add(
			"group_notify",
			self.channel_name
		)
		await self.channel_layer.group_add(
			"uid_" + str(self.scope['user'].id),
			self.channel_name
		)
		await self.accept()

	async def disconnect(self, close_code):
		await self.offline(self.scope['user'])
		await self.channel_layer.group_discard(
			"group_notify",
			self.channel_name
		)
		await self.channel_layer.group_discard(
			"uid_" + str(self.scope['user'].id),
			self.channel_name
		)

	async def send_notification(self, event):
		await self.send(text_data=json.dumps({ 'message': event['message'] }))

	async def delete_notification(self, event):
		await self.send(text_data=json.dumps({ 'message': event['message'] }))

	async def user_update(self, event):
		await self.send(text_data=json.dumps({ 'message': event['message'] }))

	@sync_to_async
	def offline(self, user):
		user.update_status('Offline')