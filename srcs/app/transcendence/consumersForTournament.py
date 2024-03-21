from typing import List

import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import logging
import asyncio
import random

logger = logging.getLogger(__name__)

class Player():
	def __init__(self, number: int, username, mmr, websocket):
		numberInTournament:int = number
		self.username = username
		self.mmr = mmr
		self.socket = websocket

class Tournament:
	def __init__(self, id: str, playersNeeded: int):
		self.id: str = str
		self.playersNeeded: int = playersNeeded
		self.players: List[Player] = []
		self.activated = False

	async def tournamentLoop():
		pass

class Storage:
	def __init__(self):
		self.tournaments: List[Tournament] = []

	def activate(self):
		for tournament in self.tournaments:
			if len(tournament.players) == tournament.playersNeeded:
				tournament.activated = True
				asyncio.create_task(tournament.tournamentLoop())


pong = Storage()
ticTacToe = Storage()

def parseMessage(message: dict, socket: AsyncWebsocketConsumer):
    pass

class TicTacToeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        message = { 'message': 'TicTacToe connection etablished !' }
        await self.send(json.dumps(message))

    async def disconnect(self, close_code):
        await self.close(close_code)

    async def receive(self, text_data):
        message: dict = json.loads(text_data)
        response = parseMessage(message, self)
        if response:
            await self.send(json.dumps(response))

# IGNORE CA MATHIEU IL VA ETRE DEPLACER
class TournamentConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.game_id = self.scope['url_route']['kwargs']['game_id']
		await self.accept()
		data = { 'message': 'Connection etablished !' }
		await self.channel_layer.group_add(
			"tournament_" + str(self.game_id),
			self.channel_name
		)
		await self.send(text_data=json.dumps(data))

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			"tournament_" + str(self.game_id),
			self.channel_name
		)

	async def tournament_players_changed(self, event):
		message = event['message']
		logger.info(f"##### Message reçu : , {message}")
		data = {
			'action': message['action'],
			'playerCount': message['playerCount'],
			'maxPlayerCount': message['maxPlayerCount'],
			'tournamentId': message['tournamentId'],
		}
		await self.send(text_data=json.dumps(data))
