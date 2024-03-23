from typing import List

import json
from channels.generic.websocket import AsyncWebsocketConsumer

# Tournamement Dynamic Consumer
class TournamentConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.game_id = self.scope['url_route']['kwargs']['game_id']
		data = { 'message': 'Connection etablished !' }
		await self.channel_layer.group_add(
			"tournament_" + str(self.game_id),
			self.channel_name
		)
		await self.accept()
		await self.send(text_data=json.dumps(data))

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			"tournament_" + str(self.game_id),
			self.channel_name
		)

	async def tournament_players_changed(self, event):
		message = event['message']
		data = {
			'action': message['action'],
			'playerCount': message['playerCount'],
			'maxPlayerCount': message['maxPlayerCount'],
			'tournamentId': message['tournamentId'],
			'users': message['users']
		}
		await self.send(text_data=json.dumps(data))

	async def tournament_created_or_deleted(self, event):
		message = event['message']
		data = {
			'action': message['action'],
			'tournaments': message['tournaments']
		}
		await self.send(text_data=json.dumps(data))
