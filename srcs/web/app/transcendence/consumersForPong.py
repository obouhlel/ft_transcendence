import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

import asyncio
import random

# -----------------------------Classes--------------------------------
class Player():
    def __init__(self, username, side, websocket):
        self.username = username
        self.position = 0
        self.score = 0
        self.side = side
        self.socket = websocket
        
class Ball():
    def __init__(self):
        self.position = {'x': 0, 'z': 0}
        self.direction = {'x': 0, 'z': 0}

    def isPlayerHitted(self, playerPos):
        topLeft = {'x': playerPos['x'] - 0.5,
                   'z': playerPos['z'] - 1}
        botRight = {'x': playerPos['x'] + 0.5,
                    'z': playerPos['z'] + 1}
        if self.position['x'] >= topLeft['x'] and self.position['x'] <= botRight['x']:
            if self.position['z'] >= topLeft['z'] and self.position['z'] <= botRight['z']:
                self.direction['x'] = self.position['x'] - playerPos['x']
                self.direction['z'] = self.position['z'] - playerPos['z']

    def isTopBotHitted(self):
        if self.position['z'] >= 10 or self.position['z'] <= -10:
            self.direction['z'] *= -1
            
    async def isScored(self):
        if self.position['x'] >= 10 or self.position['x'] <= -10:
            if self.position['x'] >= 10:
                pong.getPlayerLeft().score += 1
            else:
                pong.getPlayerRight().score += 1
            await pong.broadcast({ 'game': 'score',
                                   'score': pong.getScoreString() })
            self.reset()

    async def move(self, playersPos):
        if self.direction['x'] == 0:
            self.reset()
        else:
            self.isPlayerHitted({ 'z': playersPos['left'], 'x': -9 })
            self.isPlayerHitted({ 'z': playersPos['right'], 'x': 9 })
            self.isTopBotHitted()
            await self.isScored()
            self.position['x'] += self.direction['x'] / 10
            self.position['z'] += self.direction['z'] / 10
        
    def reset(self):
        self.position = {'x': 0, 'z': 0}
        self.direction = {'x': random.choice([-1, 1]), 'z': 0}

class Game():
    def __init__(self):
        self.__players = []
        self.__ball = Ball()
        
    def getPlayersUsername(self):
        return [player.username for player in self.__players]
        
    def getPlayer(self, username):
        for player in self.__players:
            if player.username == username:
                return player
        return None
    
    def getPlayerLeft(self):
        for player in self.__players:
            if player.side == 'left':
                return player
            
    def getPlayerRight(self):
        for player in self.__players:
            if player.side == 'right':
                return player
            
    def getOtherPlayer(self, username):
        for player in self.__players:
            if player.username != username:
                return player
        return None
    
    def getScoreString(self):
        scoreString = str(self.getPlayerLeft().score) + ' - ' + str(self.getPlayerRight().score)
        return scoreString
 
    def getLen(self):
        return len(self.__players)

    def append(self, player):
        self.__players.append(player)

    def remove(self, username):
        self.__players = [player for player in self.__players if player.username != username]

    async def broadcast(self, message):
        message = json.dumps(message)
        for player in self.__players:
            await player.socket.send(message)
            
    async def game(self):
        playersPos = {'left': self.getPlayerLeft().position, 'right': self.getPlayerRight().position}
        await self.__ball.move(playersPos)
        await self.broadcast({ 'game': 'ball position',
                         'positionX': self.__ball.position['x'], 
                         'positionZ': self.__ball.position['z'] })

pong = Game()
isLeftAdded = False

# -----------------------------Json Message--------------------------------
def getGameStartJson(side):
    return json.dumps({ 'game': 'starting',
                        'side': side })
    
def getOtherPlayerPositionJson(position):
    return json.dumps({ 'game': 'player position',
                        'position': position })

# -----------------------------Loop--------------------------------
async def gamePong():
    while True:
        if pong.getPlayerLeft().score == 10 or pong.getPlayerRight().score == 10:
            return
        await pong.game()
        await asyncio.sleep(0.01)

# -----------------------------Parser--------------------------------
def assignSide():
    global isLeftAdded
    if isLeftAdded == False:
        isLeftAdded = True
        return 'left'
    else:
        isLeftAdded = False
        asyncio.create_task(gamePong())
        return 'right'

def starting(self, message):
    newPlayer = Player(message['username'], assignSide(), self)
    pong.append(newPlayer)
    return getGameStartJson(newPlayer.side)

def playerPosition(message):
    player = pong.getPlayer(message['username'])
    player.position = message['position']
    otherPlayer = pong.getOtherPlayer(message['username'])
    return getOtherPlayerPositionJson(otherPlayer.position)
      
def score(message):
    global isScoreChange
    otherPlayer = pong.getOtherPlayer(message['username'])
    otherPlayer.score += 1
    isScoreChange = True

def forfait(message):
    otherPlayer = pong.getOtherPlayer(message['username'])
    otherPlayer.score = 10

def parseMessage(self, message):
    if 'game' in message:
        if message['game'] == 'starting':
            return starting(self, message)
        elif message['game'] == 'player position':
            return playerPosition(message)
        elif message['game'] == 'score':
            score(message)
        elif message['game'] == 'leaved':
            forfait(message)
        return json.dumps({ 'game': 'ok' })
    return json.dumps({ 'error': 'Invalid token' })

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        data = { 'message': 'Pong connection etablished !' }
        await self.send(text_data=json.dumps(data))

    async def disconnect(self, close_code):
        await self.close(close_code)

    async def receive(self, text_data):
        message = json.loads(text_data)
        response = parseMessage(self, message)
        await self.send(response)