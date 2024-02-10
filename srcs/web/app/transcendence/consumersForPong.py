import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

class PongConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        data = { 'message': 'Pong connection etablished !' }
        self.send(text_data=json.dumps(data))

    def disconnect(self, close_code):
        self.close(close_code)

    def receive(self, text_data):
        message = json.loads(text_data)
        # response = parse_message(message)
        # self.send(response)
        self.send("pong")

    def createGame(self, message):
        pass

    def send_message(self, message):
        data = { 'message': message }
        self.send(text_data=json.dumps(data))