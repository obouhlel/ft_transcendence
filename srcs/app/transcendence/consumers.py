import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

import asyncio
import uuid
from . import routing
from . import consumersForPong
from . import consumersForTicTacToe

import logging
logger = logging.getLogger(__name__)

# -----------------------------Classes--------------------------------
class Player():
	def __init__(self, username, mmr, websocket):
		self.username = username
		self.mmr = mmr
		self.socket = websocket

class Game():
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

playersConnected = Game()
playersPong = Game()
playersTicTacToe = Game()

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
	players = playersConnected.getPlayersUsername()
	return json.dumps({ 'matchmaking': 'waitlist joined',
						'username': username,
						'game': game,
	  					'players': players })
 
def getMatchmackingLeaveJson(username, game):
	players = playersConnected.getPlayersUsername()
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
	elif game == "TicTacToe":
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
			url = createUrlPattern("TicTacToe")
			for player in duoPlayers:
				await player.socket.send(getMatchFoundJson("TicTacToe", url))
		await asyncio.sleep(1)

# -----------------------------Parser--------------------------------
def register(socket, message):
	newPlayer = Player(message['username'], 0, socket)
	playersConnected.append(newPlayer)
	return getRegisterJson(newPlayer.username)
 
def unregister(message):
	playersConnected.remove(message['username'])
	return getUnregisterJson(message['username'])

def matchmakingJoined(message):
	if message['game'] == 'pong':
		player = playersConnected.getPlayer(message['username'])
		player.mmr = message['mmr']
		playersPong.append(player)
		if playersPong.getLen() == 1:
			asyncio.create_task(matchmakingPong())
	if message['game'] == 'TicTacToe':
		player = playersConnected.getPlayer(message['username'])
		player.mmr = message['mmr']
		playersTicTacToe.append(player)
		if playersTicTacToe.getLen() == 1:
			asyncio.create_task(matchmackingTicTacToe())
	return getMatchmackingJoinJson(message['username'], message['game'])

def matchmakingLeaved(message):
	if message['game'] == 'pong':
		playersPong.remove(message['username'])
	elif message['game'] == 'TicTacToe':
		playersTicTacToe.remove(message['username'])
	return getMatchmackingLeaveJson(message['username'], message['game'])

def parseMessage(self, message):
	if 'register' in message:
		if message['register'] == 'in':
			return register(self, message)
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
		data = { 'message': 'Connection etablished !' }
		await self.send(text_data=json.dumps(data))

	async def disconnect(self, close_code):
		await self.close(close_code)

	async def receive(self, text_data):
		message = json.loads(text_data)
		response = parseMessage(self, message)
		await self.send(response)

#-----------------------------NotifyConsumer--------------------------------

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
