import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

import asyncio
import uuid
from . import routing
from . import consumersForPong
from . import consumersForTicTacToe
from transcendence.models import Game, UserInLobby, Party, Lobby
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random

import logging
logger = logging.getLogger(__name__)

# -----------------------------Json Message--------------------------------
def getMatchFoundJson(game, url):
	return json.dumps({ 'matchmaking': 'match found',
						'game': game.lower(),
						'url': url })
 
def getRegisterJson(username):
	return json.dumps({ 'register': 'connected'})
 
def getUnregisterJson(username):
	return json.dumps({ 'register': 'disconnected',})
 
def getMatchmackingJoinJson(username, game):
	return json.dumps({ 'matchmaking': 'waitlist joined'})
 
def getMatchmackingLeaveJson(username, game):
	return json.dumps({ 'matchmaking': 'waitlist leaved'})

# -----------------------------Matchmaking--------------------------------
def createUrlPattern(game):
	url = "ws/" + game + "/" + str(uuid.uuid4())
	newPattern = r"^" + url + "$"
	newConsumer = None
	if game == "pong":
		newConsumer = consumersForPong.PongConsumer.as_asgi()
	elif game == "tictactoe":
		newConsumer = consumersForTicTacToe.TicTacToeConsumer.as_asgi()
	logger.info(f"New pattern: {newPattern}")
	logger.info(f"New consumer: {newConsumer}")
	routing.add_urlpattern(newPattern, newConsumer)
	return url

def makeParty(lobby):
	compatible = None
	now = timezone.now()
	#example: if the player wait for 1 second, the tolerance is 10%
	#if the player wait for 2 seconds, the tolerance is 20%
	#if the player wait for 3 seconds, the tolerance is 30%

	for user in lobby.users.all():
		user_in_lobby = UserInLobby.objects.get(user=user, lobby=lobby)
		if user_in_lobby.entry_at is None:
			user_in_lobby.entry_at = now
			user_in_lobby.save()
		waiting_time = now - user_in_lobby.entry_at
		toleance =  waiting_time.seconds / 10
		if user.stats.filter(game=lobby.game).get().nb_played == 0:
			user_ratio = 0
		else:
			user_ratio = user.stats.filter(game=lobby.game).get().nb_win/user.stats.filter(game=lobby.game).get().nb_played
		#find the most compatible users with the acceptable tolerance
		for user2 in lobby.users.all():
			if user2 != user:
				if user2.stats.filter(game=lobby.game).get().nb_played == 0:
					user2_ratio = 0
				else:
					user2_ratio = user2.stats.filter(game=lobby.game).get().nb_win/user2.stats.filter(game=lobby.game).get().nb_played
				if compatible == None:
					compatible = user2
				else:
					ratio = abs(user2_ratio - user_ratio)
					if ratio < toleance:
						compatible = user2
						break
				if compatible:
					party = Party.objects.create(game=lobby.game, player1=user, player2=compatible, started_at=timezone.now())
					lobby.users.remove(user)
					lobby.users.remove(compatible)
					return party
@sync_to_async
def  xxx():
	for game in Game.objects.all():
			if  game.lobby.users.count() >= 2:
				party =  makeParty(game.lobby)
				url = createUrlPattern(game.name.lower())
				channel_layer = get_channel_layer()
				async_to_sync(channel_layer.group_send)(
					"game__uid_" + str(party.player1.id),
					{
						"type": "startParty",
						"message":getMatchFoundJson(game.name, url)
					}
				)
				async_to_sync(channel_layer.group_send)(
					"game__uid_" + str(party.player2.id),
					{
						"type": "startParty",
						"message":getMatchFoundJson(game.name, url)
					}
				)

async def matchmaking():
	while True:
		await xxx()
		await asyncio.sleep(1)

# -----------------------------Parser--------------------------------
@sync_to_async
def matchmakingJoined(socket,message):
	gameId = message.get('gameId')
	if gameId is None:
		return json.dumps({ 'error': 'Invalid message' })
	if not Game.objects.filter(id=gameId).exists():
		return json.dumps({ 'error': 'Invalid message' })
	user = socket.user
	user.joinLobby(gameId)
	return getMatchmackingJoinJson(socket.user.username, gameId)

@sync_to_async
def matchmakingLeaved(socket, message):
	gameId = message.get('gameId')
	if gameId is None:
		return json.dumps({ 'error': 'Invalid message' })
	if not Game.objects.filter(id=gameId).exists():
		return json.dumps({ 'error': 'Invalid message' })
	user = socket.user
	user.leaveLobby(gameId)
	return getMatchmackingLeaveJson(socket.user.username, gameId)


async def parseMessage(self, message):
	if 'matchmaking' in message:
		if message['matchmaking'] == 'join':
			return await  matchmakingJoined(self, message)
		elif message['matchmaking'] == 'leave':
			return await matchmakingLeaved(self, message)
	return json.dumps({ 'error': 'Invalid token' })

class MatchmakingConsumer(AsyncWebsocketConsumer):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		asyncio.create_task(matchmaking())

	async def connect(self):
		await self.accept()
		await self.channel_layer.group_add(
			"game__uid_" + str(self.scope['user'].id),
			self.channel_name
		)
		self.user = self.scope['user']
		data = { 'message': 'Connection etablished !' }
		await self.send(text_data=json.dumps(data))

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			"game__uid_" + str(self.scope['user'].id),
			self.channel_name
		)
		await self.close(close_code)

	async def receive(self, text_data):
		message = json.loads(text_data)
		response = await parseMessage(self, message)
		logger.info(response)
		await self.send(response)

	async def startParty(self, event):
		await self.send(text_data=event['message'])

