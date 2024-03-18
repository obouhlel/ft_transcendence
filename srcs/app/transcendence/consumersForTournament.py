from typing import List

import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

import asyncio
import random

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