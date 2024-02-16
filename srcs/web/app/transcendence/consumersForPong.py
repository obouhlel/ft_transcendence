import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

import asyncio
import random

playersPong = []

isLeftAdded = False

def createSelf(self, message):
    global isLeftAdded
    self.username = message['username']
    self.position = 0
    self.score = 0
    if not isLeftAdded:
        self.side = 'left'
        isLeftAdded = True
    else:
        self.side = 'right'

def starting(self, message):
    createSelf(self, message)
    return json.dumps({ 'game': 'starting',
                        'side': self.side })

def position(self, message):
    self.position = message['position']
    if playersPong[0].username == message['username']:
        return json.dumps({ 'game': 'position',
                            'position': playersPong[1].position })
    elif playersPong[1].username == message['username']:
        return json.dumps({ 'game': 'position',
                            'position': playersPong[0].position })
    return json.dumps({ 'error': 'Username doesnt exist' })
            
def parseMessage(self, message):
    if 'game' in message:
        if 'username' in message:
            if message['game'] == 'starting':
                return starting(self, message)
            elif message['game'] == 'position':
                return position(self, message)
            elif message['game'] == 'score':
                return
            elif message['game'] == 'end':
                return
        return json.dumps({ 'error': 'no username for game' })
    return json.dumps({ 'error': 'Invalid token' })

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        playersPong.append(self)
        await self.accept()
        data = { 'message': 'Pong connection etablished !' }
        await self.send(text_data=json.dumps(data))

    async def disconnect(self, close_code):
        await self.close(close_code)

    async def receive(self, text_data):
        message = json.loads(text_data)
        response = parseMessage(self, message)
        await self.send(response)