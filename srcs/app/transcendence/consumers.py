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
	def __init__(self, username, mmr, websocket):
		self.username = username
		self.mmr = mmr
		self.socket = websocket

class GameX():
	def __init__(self):
		self.__players = []
  
	def getPlayersUsername(self):
		return [player.username for player in self.__players]
		
	def getPlayer(self, username):
		for player in self.__players:
			if player.username == username:
				return player
		return None
 
	def __sort (self):
		self.__players = sorted(self.__players, key=lambda player: player.mmr)
 
	def getLen(self):
		return len(self.__players)

	def append(self, player):
		self.__players.append(player)
		self.__sort()
	
	def pop(self, index):
		return self.__players.pop(index)

	def remove(self, username):
		self.__players = [player for player in self.__players if player.username != username]

	def doDuo(self):
		duoPlayers = []
		duoPlayers.append(self.pop(0))
		duoPlayers.append(self.pop(0))
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
	return json.dumps({ 'register': 'connected',
						'username': username })
 
def getUnregisterJson(username):
	return json.dumps({ 'register': 'disconnected',
						'username': username })
 
def getMatchmackingJoinJson(username, game):
	players = playersTicTacToe.getPlayersUsername()
	return json.dumps({ 'matchmaking': 'waitlist joined',
						'username': username,
						'game': game,
	  					'players': players })
 
def getMatchmackingLeaveJson(username, game):
	players = playersTicTacToe.getPlayersUsername()
	return json.dumps({ 'matchmaking': 'waitlist leaved',
						'username': username,
						'game': game,
						'players': players })

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




async def matchmakingPong():
	while True:
		if playersPong.getLen() == 0:
			return
		if playersPong.getLen() >= 2:
			duoPlayers = playersPong.doDuo()
			url = createUrlPattern("pong")
			for player in duoPlayers:
				await player.socket.send(getMatchFoundJson("pong", url))
		await asyncio.sleep(1)

async def matchmackingTicTacToe():
	while True:
		if playersTicTacToe.getLen() == 0:
			return
		if playersTicTacToe.getLen() >= 2:
			duoPlayers = playersTicTacToe.doDuo()
			url = createUrlPattern("ticTacToe")
			for player in duoPlayers:
				await player.socket.send(getMatchFoundJson("ticTacToe", url))
		await asyncio.sleep(1)

# -----------------------------Parser--------------------------------
@sync_to_async
def register(socket, message):
	game_id = message['gameId']

	socket.user = socket.scope['user']
	if socket.user.joinLobby(game_id) == None:
		return json.dumps({ 'error': 'You can not join this game' })
	newPlayer = Player(socket.user.username, 0, socket)
	playersConnected.append(newPlayer)
	return getRegisterJson(newPlayer.username)
 
def unregister(socket, message):
	playersConnected.remove(socket.user.username)
	playersPong.remove(socket.user.username)
	playersTicTacToe.remove(socket.user.username)
	return getUnregisterJson(socket.user.username)

def matchmakingJoined(socket,message):
	if message['game'] == 'pong':
		player = playersConnected.getPlayer(socket.user.username)
		playersPong.append(player)
		if playersPong.getLen() == 1:
			asyncio.create_task(matchmakingPong())
	if message['game'] == 'ticTacToe':
		player = playersConnected.getPlayer(socket.user.username)
		playersTicTacToe.append(player)
		if playersTicTacToe.getLen() == 1:
			asyncio.create_task(matchmackingTicTacToe())
	return getMatchmackingJoinJson(socket.user.username, message['game'])

def matchmakingLeaved(socket, message):
	if message['game'] == 'pong':
		playersPong.remove(socket.user.username)
	elif message['game'] == 'ticTacToe':
		playersTicTacToe.remove(socket.user.username)
	return getMatchmackingLeaveJson(socket.user.username, message['game'])


async def parseMessage(self, message):
	if 'register' in message:
		if message['register'] == 'in':
			return await register(self, message)
		elif message['register'] == 'out':
			return unregister(message)

	if 'matchmaking' in message:
		if message['matchmaking'] == 'join':
			return matchmakingJoined(message)
		elif message['matchmaking'] == 'leave':
			return matchmakingLeaved(message)
	return json.dumps({ 'error': 'Invalid token' })

class MatchmakingConsumer(AsyncWebsocketConsumer):
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