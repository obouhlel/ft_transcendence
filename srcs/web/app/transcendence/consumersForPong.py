import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

import asyncio
import random

playersPong = []

isLeftAdded = False
isBallMoving = False

# -----------------------------Getters--------------------------------
def getOtherPlayer(self):
    if playersPong[0].username == self.username:
        return playersPong[1]
    elif playersPong[1].username == self.username:
        return playersPong[0]

def getPlayerLeft():
    for player in playersPong:
        if player.side == 'left':
            return player
        
def getPlayerRight():
    for player in playersPong:
        if player.side == 'right':
            return player

def getScoreString(message):
    scoreString = str(getPlayerLeft().score) + ' - ' + str(getPlayerRight().score)
    return scoreString

# -----------------------------Loop--------------------------------
async def broadcast(message):
    message = json.dumps(message)
    for player in playersPong:
        await player.send(message)
        
async def sendPosition():
    playerLeft = getPlayerLeft()
    playerRight = getPlayerRight()
    await playerLeft.send(json.dumps({ 'game': 'player position',
                                       'position': playerRight.position }))
    await playerRight.send(json.dumps({ 'game': 'player position',
                                        'position': playerLeft.position }))
    
async def findWinner():
    if getPlayerLeft().score == 10:
        message = { 'game': 'end',
                    'score': getScoreString(),
                    'winner': getPlayerLeft().username }
        await broadcast(message)
        return True
    elif getPlayerRight().score == 10:
        message = { 'game': 'end',
                    'score': getScoreString(),
                    'winner': getPlayerRight().username }
        await broadcast(message)
        return True
    return False

async def gamePong():
    while True:
        global isBallMoving
        if await findWinner() == True:
            playersPong.clear()
            return
        await sendPosition()
        if isBallMoving == False:
            message = { 'game': 'start ball', 
                        'direction': random.choice([-1, 1]) }
            await broadcast(message)
            isBallMoving = True
        await asyncio.sleep(0.1)


# -----------------------------Parser--------------------------------
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
    return json.dumps({ 'game': 'ok player position'})
      
def score(self):
    getOtherPlayer(self).score += 1
    return json.dumps({ 'game': 'ok score' })

def forfait(self):
    playerWinner = getOtherPlayer(self)
    playerWinner.score = 10
    return json.dumps({ 'game': 'ok forfait' })

def parseMessage(self, message):
    if 'game' in message:
        if 'username' in message:
            if message['game'] == 'starting':
                return starting(self, message)
            elif message['game'] == 'player position':
                return playerPosition(self, message)
            elif message['game'] == 'score':
                return score(self, message)
            elif message['game'] == 'leaved':
                return forfait(self, message)
        return json.dumps({ 'error': 'no username for game' })
    return json.dumps({ 'error': 'Invalid token' })

# -----------------------------Consumer--------------------------------
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