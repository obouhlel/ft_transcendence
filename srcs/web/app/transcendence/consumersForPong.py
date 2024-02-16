import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

import asyncio
import random

playersPong = []

isLeftAdded = False
isBallMoving = False

async def gamePong():
    while True:
        global isBallMoving
        if isBallMoving == False:
            message = { 'game': 'start ball', 
                        'direction': random.choice([-1, 1]) }
            await playersPong[0].send(json.dumps(message))
            await playersPong[1].send(json.dumps(message))
            isBallMoving = True
        await asyncio.sleep(1)

def createSelf(self, message):
    global isLeftAdded
    self.username = message['username']
    self.position = 0
    self.score = 0
    if isLeftAdded == False:
        self.side = 'left'
        isLeftAdded = True
    else:
        self.side = 'right'
        isLeftAdded = False
        asyncio.create_task(gamePong())

def starting(self, message):
    createSelf(self, message)
    return json.dumps({ 'game': 'starting',
                        'side': self.side })

def playerPosition(self, message):
    self.position = message['position']
    if playersPong[0].username == message['username']:
        return json.dumps({ 'game': 'player position',
                            'position': playersPong[1].position })
    elif playersPong[1].username == message['username']:
        return json.dumps({ 'game': 'player position',
                            'position': playersPong[0].position })
    return json.dumps({ 'error': 'Username doesnt exist' })

def updateScore(message, indPlayerScorer):
    playersPong[indPlayerScorer].score += 1
    messageForScorer = json.dump({ 'game': 'score',
                                   'score': 'you' })
    message = json.dump({ 'game': 'score',
                          'score': 'opponent' })
    playersPong[indPlayerScorer].send(messageForScorer)
    return message
      
def score(message):
    if playersPong[0].username == message['username']:
        return updateScore(message, 1)
    elif playersPong[1].username == message['username']:
        return updateScore(message, 0)
            
def parseMessage(self, message):
    if 'game' in message:
        if 'username' in message:
            if message['game'] == 'starting':
                return starting(self, message)
            elif message['game'] == 'player position':
                return playerPosition(self, message)
            elif message['game'] == 'score':
                return score(message)
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