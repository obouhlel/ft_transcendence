import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

import random

playersPong = []

def parse_message(message):
    if 'game' in message:
        if 'username' in message:
            if message['game'] == 'starting':
                if len(playersPong) != 2:
                    playersPong.append({'player': message['username'], 'side': 'not assigned', "position": 0, 'score': 0})
                elif len(playersPong) == 2 and playersPong[0]['side'] == 'not assigned' and playersPong[1]['side'] == 'not assigned':
                    playersPong[1]['side'] = 'left'
                    playersPong[0]['side'] = 'right'
                for player in playersPong:
                    if player['player'] == message['username']:
                        return json.dumps({ 'game': 'starting', 'side': player['side'] })
                return json.dumps({ 'game': 'wait other player' })
            elif message['game'] == 'position':
                if message['username'] == playersPong[0]['player']:
                    playersPong[0]['position'] = message['position']
                    return json.dumps({ 'game': 'position', 'position': playersPong[1]['position'] })
                elif message['username'] == playersPong[1]['player']:
                    playersPong[1]['position'] = message['position']
                    return json.dumps({ 'game': 'position', 'position': playersPong[0]['position'] })
            elif message['game'] == 'score':
                return
            elif message['game'] == 'end':
                return
        return json.dumps({ 'error': 'no username for game' })
    return json.dumps({ 'error': 'Invalid token' })

class PongConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        data = { 'message': 'Pong connection etablished !' }
        self.send(text_data=json.dumps(data))

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