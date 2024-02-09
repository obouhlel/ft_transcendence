import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

def parse_message(message):
	if 'matchmaking' in message:
		if message['matchmaking'] == 'join':
			return json.dumps({ 'matchmaking': 'waitlist joined' })
		elif message['matchmaking'] == 'leave':
			return json.dumps({ 'matchmaking': 'waitlist leaved' })

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