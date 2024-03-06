from typing import List

import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

import asyncio
import random

# -----------------------------Classes--------------------------------
class Player():
    def __init__(self, username, side, websocket):
        self.username: str = username
        self.position: float = 0
        self.score: int = 0
        self.memScore: int = 0
        self.side: str = side
        self.socket: AsyncWebsocketConsumer = websocket
        self.disconnected: bool = False

class Ball():
    def __init__(self):
        self.position = {'x': 0, 'z': 0}
        self.direction = {'x': 0, 'z': 0}

    def isPlayerHitted(self, playerPos: float):
        topLeft = {'x': playerPos['x'] - 0.5,
                   'z': playerPos['z'] - 1}
        botRight = {'x': playerPos['x'] + 0.5,
                    'z': playerPos['z'] + 1}
        if self.position['x'] >= topLeft['x'] and self.position['x'] <= botRight['x']:
            if self.position['z'] >= topLeft['z'] and self.position['z'] <= botRight['z']:
                self.direction['x'] = self.position['x'] - playerPos['x']
                self.direction['z'] = self.position['z'] - playerPos['z']
                maxVal = max(abs(self.direction['x']), abs(self.direction['z']))
                if maxVal != 0:
                    self.direction['x'] /= maxVal
                    self.direction['z'] /= maxVal

    def isTopBotHitted(self):
        if self.position['z'] >= 10 or self.position['z'] <= -10:
            self.direction['z'] *= -1
            
    def isScored(self, players: dict[str, Player]):
        if self.position['x'] >= 10 or self.position['x'] <= -10:
            if self.position['x'] >= 10:
                players['left'].score += 1
            else:
                players['right'].score += 1
            self.reset()

    def move(self, players: dict[str, Player]):
        if self.direction['x'] == 0:
            self.reset()
        else:
            self.isPlayerHitted({ 'z': players['left'].position, 'x': -9 })
            self.isPlayerHitted({ 'z': players['right'].position, 'x': 9 })
            self.isTopBotHitted()
            self.isScored(players)
            self.position['x'] += self.direction['x'] / 10
            self.position['z'] += self.direction['z'] / 10
        
    def reset(self):
        self.position = {'x': 0, 'z': 0}
        self.direction = {'x': random.choice([-1, 1]), 'z': 0}

class Duo():
    def __init__(self, id):
        self.id: str = id
        self.isLeftAdded: bool = False
        self.players: List[Player] = []
        self.ball: Ball = Ball()
        self.activated: bool = False
        
    def append(self, player: Player):
        self.players.append(player)
        
    def remove(self, player: Player):
        self.players.remove(player)

    def getPlayer(self, username: str):
        for player in self.players:
            if player.username == username:
                return player
        return None
    
    def getPlayerLeft(self):
        for player in self.players:
            if player.side == 'left':
                return player
        return None
    
    def getPlayerRight(self):
        for player in self.players:
            if player.side == 'right':
                return player
        return None
    
    def getOtherPlayer(self, username: str):
        for player in self.players:
            if player.username != username:
                return player
        return None
    
    def isScoreChanged(self):
        playerLeft = self.getPlayerLeft()
        playerRight = self.getPlayerRight()
        if playerLeft == None or playerRight == None:
            return True
        if playerLeft.score != playerLeft.memScore or playerRight.score != playerRight.memScore:
            playerLeft.memScore = playerLeft.score
            playerRight.memScore = playerRight.score
            return True
        return False
    
    def getScoreString(self):
        playerLeft = self.getPlayerLeft()
        playerRight = self.getPlayerRight()
        return str(playerLeft.score if playerLeft is not None else 0) + ' - ' + str(playerRight.score if playerRight is not None else 0)
        
    def isEnd(self):
        playerLeft = self.getPlayerLeft()
        playerRight = self.getPlayerRight()
        if playerLeft == None or playerRight == None:
            return True
        return playerLeft.score == 10 or playerRight.score == 10

    def isSomeoneDisconected(self):
        for player in self.players:
            if player.disconnected == True:
                return True
        return False
    
    def getDisconectedPlayer(self):
        for player in self.players:
            if player.disconnected == True:
                return player
        return None

    async def broadcast(self, message: dict):
        for player in self.players:
            await player.socket.send(json.dumps(message))
        
    async def gameLoop(self):
        while True:
            if self.isSomeoneDisconected() == True:
                disconnectedPlayer = self.getDisconectedPlayer()
                winner = self.getOtherPlayer(disconnectedPlayer.username)
                scoreString = "10 - 0" if winner.side == 'left' else "0 - 10"
                await self.broadcast({ 'game': 'end',
                                       'score': scoreString,
                                       'winner': winner.side })
                self.remove(disconnectedPlayer)
                self.remove(winner)
                return
            playerLeft = self.getPlayerLeft()
            playerRight = self.getPlayerRight()
            if playerLeft != None and playerRight != None:
                self.ball.move({ 'left': playerLeft,
                                 'right': playerRight })
                await self.broadcast({ 'game': 'positions',
                                       'positionBallX': self.ball.position['x'],
                                       'positionBallZ': self.ball.position['z'],
                                       'playerLeft': playerLeft.position,
                                       'playerRight': playerRight.position })
            if self.isScoreChanged():
                await self.broadcast({ 'game': 'score',
                                       'score': self.getScoreString() })
            if self.isEnd():
                await self.broadcast({ 'game': 'end',
                                       'winner': playerLeft.score == 10 and 'left' or 'right' })
                return
            await asyncio.sleep(0.01)
    
class Game():
    def __init__(self):
        self.duos: List[Duo] = []
    
    def append(self, duo: Duo):
        self.duos.append(duo)
        self.activate()
        
    def remove(self, duo: Duo):
        self.duos.remove(duo)
    
    def getDuo(self, id: str):
        for duo in self.duos:
            if duo.id == id:
                return duo
        return None
    
    def isDuoFull(self, id: str=None):
        if id != None:
            duo = self.getDuo(id)
            if duo:
                return len(duo.players) == 2
        for duo in self.duos:
            if len(duo.players) == 2:
                return True
    
    def activate(self):
        for duo in self.duos:
            if len(duo.players) == 2 and duo.activated == False:
                duo.activated = True
                asyncio.create_task(duo.gameLoop())
            elif len(duo.players) == 0:
                self.remove(duo)

pong = Game()

def assignSide(duo: Duo):
    if duo.isLeftAdded == False:
        duo.isLeftAdded = True
        return 'left'
    return 'right'

def assignDuo(message: dict, socket: AsyncWebsocketConsumer):
    duo = pong.getDuo(message['id'])
    if duo == None:
        duo = Duo(message['id'])
    player = Player(message['username'], assignSide(duo), socket)
    duo.append(player)
    pong.append(duo)
    return { 'game': 'starting',
             'side': player.side } 

def leaveDuo(message: dict):
    duo = pong.getDuo(message['id'])
    if duo != None:
        player = duo.getPlayer(message['username'])
        if player != None:
            player.disconnected = True
    return None

def position(message: dict):
    duo = pong.getDuo(message['id'])
    if duo:
        player = duo.getPlayer(message['username'])
        if player != None:
            player.position = message['position']
    return None

def parseMessage(message: dict, socket: AsyncWebsocketConsumer):
    if 'game' in message:
        if message['game'] == 'starting':
            return assignDuo(message, socket)
        if message['game'] == 'leaved':
            return leaveDuo(message)
        if message['game'] == 'player position':
            return position(message)
    return { 'error': 'Invalid message' }

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        message = { 'message': 'Pong connection etablished !' }
        await self.send(json.dumps(message))

    async def disconnect(self, close_code):
        await self.close(close_code)

    async def receive(self, text_data):
        message: dict = json.loads(text_data)
        response = parseMessage(message, self)
        if response:
            await self.send(json.dumps(response))