import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

class MatchmakingConsumer(WebsocketConsumer):
	def connect(self):
		self.accept()

		data = { 'message': 'Connection etablished !' }
		self.send(text_data=json.dumps(data))
		print('Connection etablished, with the client !', self)

	def disconnect(self, close_code):
		self.close(close_code)

	def receive(self, text_data):
		test_data_json = json.loads(text_data)
		message = test_data_json['message']
		print(message)
		self.send_message(message)

	def waiting_other_player(self, message):
		pass

	def send_message(self, message):
		data = { 'message': message }
		self.send(text_data=json.dumps(data))