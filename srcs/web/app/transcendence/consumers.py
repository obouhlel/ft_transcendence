import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

import asyncio
import uuid
from . import routing
from . import consumersForPong

playersConnected = []

playersPong = []
playersShooter = []

def createUrlPattern(url):
	newPattern = r"^" + url + "$"
	newConsumer = consumersForPong.PongConsumer.as_asgi()
	routing.add_urlpattern(newPattern, newConsumer)

def getPlayersConnectedForSend():
    tmp = []
    for player in playersConnected:
        tmp.append(player.username)
    return tmp

def getPlayerSocket(username):
	for player in playersConnected:
		if player.username == username:
			return player
	return None

async def matchmakingPong():
	while True:
		if len(playersPong) == 0:
			return
		if len(playersPong) >= 2:
			duoPlayers = []
			duoPlayers.append(playersPong.pop(0))
			duoPlayers.append(playersPong.pop(0))
			url = "ws/pong/" + str(uuid.uuid4())
			createUrlPattern(url)
			for player in duoPlayers:
				playerSocket = getPlayerSocket(player)
				playersConnected.remove(playerSocket)
				await playerSocket.send(json.dumps({ 'matchmaking': 'match found',
													'game': 'pong',
													'url': url }))
		await asyncio.sleep(1)

def register(self, message):
	self.username = message['username']
	playersConnected.append(self)
	return json.dumps({ 'register': 'connected',
						'username': self.username })
 
def unregister(self, message):
	username = self.username
	playersConnected.remove(self)
	return json.dumps({ 'register': 'disconnected',
						'username': username })

def matchmakingJoined(message):
	if message['game'] == 'pong':
		playersPong.append(message['username'])
		if len(playersPong) == 1:
			asyncio.create_task(matchmakingPong())
	elif message['game'] == 'shooter':
		playersShooter.append(message['username'])
	return json.dumps({ 'matchmaking': 'waitlist joined',
                    	'username': message['username'],
                     	'players': getPlayersConnectedForSend() })

def matchmakingLeaved(message):
	if message['game'] == 'pong':
		playersPong.remove(message['username'])
	elif message['game'] == 'shooter':
		playersShooter.remove(message['username'])
	return json.dumps({ 'matchmaking': 'waitlist leaved',
                    	'username': message['username'],
                     	'players': getPlayersConnectedForSend() })

def parse_message(self, message):
	if 'register' in message:
		if 'username' in message:
			if message['register'] == 'in':
				return register(self, message)
			elif message['register'] == 'out':
				return unregister(self, message)

	if 'matchmaking' in message:
		if 'username' in message:
			if 'game' in message:
				if message['matchmaking'] == 'join':
					return matchmakingJoined(message)
				elif message['matchmaking'] == 'leave':
					return matchmakingLeaved(message)
				return json.dumps({ 'error': 'Invalid matchmaking keyword' })
			return json.dumps({ 'error': 'no game for matchmaking' })
		return json.dumps({ 'error': 'no username for matchmaking' })
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
		response = parse_message(self, message)
		await self.send(response)