import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

import uuid
from . import routing
from . import consumersForPong

playersPong = []
playersShooter = []

playersGameObj = []

def createUrlPattern(roomID):
	newPattern = r"^" + roomID + "$"
	newConsumer = consumersForPong.PongConsumer.as_asgi()
	routing.add_urlpattern(newPattern, newConsumer)

def matchmakingJoined(message):
	if message['game'] == 'pong':
		playersPong.append(message['username'])
	elif message['game'] == 'shooter':
		playersShooter.append(message['username'])
	return json.dumps({ 'matchmaking': 'waitlist joined', 'username': message['username'], 'players': playersPong})

def matchmakingLeaved(message):
	if message['game'] == 'pong':
		playersPong.remove(message['username'])
	elif message['game'] == 'shooter':
		playersShooter.remove(message['username'])
	return json.dumps({ 'matchmaking': 'waitlist leaved', 'username': message['username'], 'players': playersPong})

def matchmakingStatus(message):
	needToBeRedirect = False
	for gameObj in playersGameObj:
		if message['username'] == gameObj['player1'] or message['username'] == gameObj['player2']:
			if message['username'] == gameObj['player1']:
				gameObj['player1'] = "assigned"
			elif message['username'] == gameObj['player2']:
				gameObj['player2'] = "assigned"
			needToBeRedirect = True
		elif gameObj['player1'] == "assigned" and gameObj['player2'] == "assigned":
			playersGameObj.remove(gameObj)
	if needToBeRedirect == True:
		return json.dumps({ 'matchmaking': 'match found', 'game': gameObj['game'], 'socketPath': gameObj['roomID']})

	if message['game'] == 'pong':
		if len(playersPong) >= 2 and message['username'] in playersPong:
			roomID = 'ws/pong/' + str(uuid.uuid4())
			gameObj = { 'game': 'pong', 'roomID': roomID, 'player1': playersPong.pop(0), 'player2': playersPong.pop(0) }
			playersGameObj.append(gameObj)
			createUrlPattern(roomID)
	elif message['game'] == 'shooter':
		if len(playersShooter) >= 2 and message['username'] in playersShooter:
			roomID = 'ws/shooter/' + str(uuid.uuid4())
			gameObj = { 'game': 'shooter', 'roomID': roomID, 'player1': playersShooter.pop(0), 'player2': playersShooter.pop(0) }
			playersGameObj.append(gameObj)
			createUrlPattern(roomID)

	return json.dumps({ 'matchmaking': 'on waitlist', 'game': message['game']})

def parse_message(message):
	if 'matchmaking' in message:
		if 'username' in message:
			if 'game' in message:
				if message['matchmaking'] == 'join':
					return matchmakingJoined(message)
				elif message['matchmaking'] == 'leave':
					return matchmakingLeaved(message)
				elif message['matchmaking'] == 'status':
					return matchmakingStatus(message)
				return json.dumps({ 'error': 'Invalid matchmaking keyword' })
			return json.dumps({ 'error': 'no game for matchmaking' })
		return json.dumps({ 'error': 'no username for matchmaking' })
	return json.dumps({ 'error': 'Invalid token' })

class MatchmakingConsumer(WebsocketConsumer):
	def connect(self):
		self.accept()
		data = { 'message': 'Connection etablished !' }
		self.send(text_data=json.dumps(data))
		print('Connection etablished, with the client !', self)

	def disconnect(self, close_code):
		self.close(close_code)

	def receive(self, text_data):
		message = json.loads(text_data)
		response = parse_message(message)
		self.send(response)

	def createGame(self, message):
		pass

	def send_message(self, message):
		data = { 'message': message }
		self.send(text_data=json.dumps(data))