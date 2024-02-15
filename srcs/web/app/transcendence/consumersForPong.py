import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

import random

playersPong = []

def starting(message):
    if len(playersPong) != 2:
        playersPong.append({'player': message['username'], 'side': 'not assigned', "position": 0, 'score': 0})
    elif len(playersPong) == 2 and playersPong[0]['side'] == 'not assigned' and playersPong[1]['side'] == 'not assigned':
        playersPong[1]['side'] = 'left'
        playersPong[0]['side'] = 'right'
        for player in playersPong:
            if player['player'] == message['username']:
                return json.dumps({ 'game': 'starting', 'side': player['side'] })
    return json.dumps({ 'game': 'wait other player' })

def position(message):
    if message['username'] == playersPong[0]['player']:
        playersPong[0]['position'] = message['position']
        return json.dumps({ 'game': 'position', 'position': playersPong[1]['position'] })
    elif message['username'] == playersPong[1]['player']:
        playersPong[1]['position'] = message['position']
        return json.dumps({ 'game': 'position', 'position': playersPong[0]['position'] })
            
def parseMessage(message):
    if 'game' in message:
        if 'username' in message:
            if message['game'] == 'starting':
                return starting(message)
            elif message['game'] == 'position':
                return position(message)
            elif message['game'] == 'score':
                return
            elif message['game'] == 'end':
                return
        return json.dumps({ 'error': 'no username for game' })
    return json.dumps({ 'error': 'Invalid token' })

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.accept()
        data = { 'message': 'Pong connection etablished !' }
        self.send(text_data=json.dumps(data))

    async def disconnect(self, close_code):
        self.close(close_code)

    async def receive(self, text_data):
        message = json.loads(text_data)
        response = parseMessage(message)
        self.send(response)