import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

import asyncio
import uuid
from . import routing
from . import consumersForPong
from . import consumersForTicTacToe
from transcendence.models import Game, UserInLobby, Party

import logging
logger = logging.getLogger(__name__)

# -----------------------------Classes--------------------------------
class Player():
	def __init__(self, username, websocket):
		self.username = username
		self.socket = websocket

class GameX():
	def __init__(self):
		self.__players = set()
  
	def getPlayersUsername(self):
		return [player.username for player in self.__players]
		
	def getPlayer(self, username):
		for player in self.__players:
			if player.username == username:
				return player
		return None
 
	def getLen(self):
		return len(self.__players)

	def append(self, player):
		self.remove(player.username)
		self.__players.add(player)

	def remove(self, username):
		player_to_remove = None
		for player in self.__players:
			if player.username == username:
				player_to_remove = player
				break
		if player_to_remove:
			self.__players.remove(player_to_remove)

	def doDuo(self):
		if len(self.__players) < 2:
			return None # Not enough players to form a duo
		duoPlayers = []
		# Since sets are unordered, we need to ensure we get two different players
		for player in self.__players:
			duoPlayers.append(player)
			if len(duoPlayers) == 2:
				break
		for player in duoPlayers:
			self.__players.remove(player)
		return duoPlayers

playersConnected = GameX()
playersPong = GameX()
playersTicTacToe = GameX()

# -----------------------------Json Message--------------------------------
def getMatchFoundJson(game, url):
	return json.dumps({ 'matchmaking': 'match found',
						'game': game,
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
	elif game == "ticTacToe":
		newConsumer = consumersForTicTacToe.TicTacToeConsumer.as_asgi()
	routing.add_urlpattern(newPattern, newConsumer)
	return url




async def matchmaking():
	while True:
		if playersPong.getLen() >= 2:
			duoPlayers = playersPong.doDuo()
			url = createUrlPattern("pong")
			for player in duoPlayers:
				await player.socket.send(getMatchFoundJson("pong", url))
		if playersTicTacToe.getLen() >= 2:
			duoPlayers = playersTicTacToe.doDuo()
			url = createUrlPattern("ticTacToe")
			for player in duoPlayers:
				await player.socket.send(getMatchFoundJson("ticTacToe", url))
		await asyncio.sleep(1)

# -----------------------------Parser--------------------------------
@sync_to_async
def matchmakingJoined(socket,message):
	gameId = message.get('gameId')
	if gameId is None:
		return json.dumps({ 'error': 'Invalid message' })
	game = Game.objects.get(id=gameId)
	user = socket.user
	user.joinLobby(gameId)
	player = Player(socket.user.username, socket)
	playersConnected.append(player)
	if game.name.lower() == 'pong':
		logger.info(playersPong.getLen())
		logger.info(playersPong.getPlayersUsername())
		playersPong.append(player)
	elif game.name.lower() == 'tictactoe':
		playersTicTacToe.append(player)
	return getMatchmackingJoinJson(socket.user.username, gameId)

@sync_to_async
def matchmakingLeaved(socket, message):
	gameId = message.get('gameId')
	if gameId is None:
		return json.dumps({ 'error': 'Invalid message' })
	game = Game.objects.get(id=gameId)
	user = socket.user
	user.leaveLobby(gameId)
	player = playersConnected.getPlayer(socket.user.username)
	if game.name.lower() == 'pong':
		playersPong.remove(player)
	elif game.name.lower() == 'tictactoe':
		playersTicTacToe.remove(player)
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
		self.user = self.scope['user']
		data = { 'message': 'Connection etablished !' }
		await self.send(text_data=json.dumps(data))

	async def disconnect(self, close_code):
		await self.close(close_code)

	async def receive(self, text_data):
		message = json.loads(text_data)
		response = await parseMessage(self, message)
		logger.info(response)
		await self.send(response)

