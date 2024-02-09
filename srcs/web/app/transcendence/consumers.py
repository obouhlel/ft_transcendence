import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

playersPong = []
playerShooter = []

def parse_message(message):
	if 'matchmaking' in message:
		if 'username' in message:
			if 'game' in message:
				if message['matchmaking'] == 'join':
					if message['game'] == 'pong':
						playersPong.append(message['username'])
					elif message['game'] == 'shooter':
						playerShooter.append(message['username'])
					return json.dumps({ 'matchmaking': 'waitlist joined', 'username': message['username'], 'players': playersPong})
				elif message['matchmaking'] == 'leave':
					if message['game'] == 'pong':
						playersPong.remove(message['username'])
					elif message['game'] == 'shooter':
						playerShooter.remove(message['username'])
					return json.dumps({ 'matchmaking': 'waitlist leaved', 'username': message['username'], 'players': playersPong})
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

	def waiting_other_player(self, message):
		pass

	def send_message(self, message):
		data = { 'message': message }
		self.send(text_data=json.dumps(data))