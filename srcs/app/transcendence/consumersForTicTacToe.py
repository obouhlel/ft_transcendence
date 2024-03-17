from typing import List

import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

import asyncio
import random
from asgiref.sync import sync_to_async
from .models import Game as GameModel, CustomUser, Party

import logging
logger = logging.getLogger(__name__)
@sync_to_async
def updateParty(winner, loser, isDraw=False):
    logger.info(f"updateParty: {winner.username} vs {loser.username}")
    game = GameModel.objects.get(name='TicTacToe')
    user1 = CustomUser.objects.get(username=winner.username)
    user2 = CustomUser.objects.get(username=loser.username)
    party = Party.objects.get(player1=user1, player2=user2, game=game, status='Waiting')
    if party is None:
        party = Party.objects.create(game=game, player1=user1, player2=user2)
    if isDraw:
        party.score1 = 1
        party.score2 = 1
    elif winner.username == user1.username:
        party.score1 = 2
        party.score2 = 0
    else:
        party.score1 = 0
        party.score2 = 2
    party.update_end()
    


class Player():
    def __init__(self, username, pawn, websocket):
        self.username: str = username
        self.pawn: str = pawn
        self.socket: AsyncWebsocketConsumer = websocket
        self.played: bool = False
        self.disconected: bool = False

class Map():
    def __init__(self):
        self.map = [['0', '0', '0'],
                    ['0', '0', '0'],
                    ['0', '0', '0']]
        self.lastPlayedPos: dict = {'x': -1, 'y': -1}

    def isFull(self):
        for row in self.map:
            for cell in row:
                if cell == '0':
                    return False
        return True

    def isWin(self, player: Player):
        for i in range(3):
            if self.map[i][0] == self.map[i][1] == self.map[i][2] == player.pawn:
                return True
            if self.map[0][i] == self.map[1][i] == self.map[2][i] == player.pawn:
                return True
        if self.map[0][0] == self.map[1][1] == self.map[2][2] == player.pawn:
            return True
        if self.map[0][2] == self.map[1][1] == self.map[2][0] == player.pawn:
            return True
        return False

    def getMapCase(self, x, y):
        return self.map[x][y]

class Duo():
    def __init__(self, id):
        self.id: str = id
        self.isXadded: bool = False
        self.turn: str = 'X'
        self.players: List[Player] = []
        self.map: Map = Map()
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
    
    def getOtherPlayer(self, username: str):
        for player in self.players:
            if player.username != username:
                return player
        return None

    def getPlayerWithPawn(self, pawn: str):
        for player in self.players:
            if player.pawn == pawn:
                return player
        return None

    def isSomeoneDisconected(self):
        for player in self.players:
            if player.disconected == True:
                return True
        return False
    
    def getDisconectedPlayer(self):
        for player in self.players:
            if player.disconected == True:
                return player
        return None

    async def broadcast(self, message: dict):
        for player in self.players:
            message['username'] = player.username
            await player.socket.send(json.dumps(message))
        
    async def gameLoop(self):
        sended = False
        while True:
            if self.isSomeoneDisconected() == True:
                disconnectedPlayer = self.getDisconectedPlayer()
                winner = self.getOtherPlayer(disconnectedPlayer.username)
                await winner.socket.send(json.dumps({ 'game': 'end',
                                                      'winner': winner.username }))
                self.remove(disconnectedPlayer)
                self.remove(winner)
                return
            playerTurn = self.getPlayerWithPawn(self.turn)
            if sended == False:
                await playerTurn.socket.send(json.dumps({ 'game': 'play' }))
                sended = True
            if playerTurn.played == True:
                otherPlayer = self.getOtherPlayer(playerTurn.username)
                await otherPlayer.socket.send(json.dumps({ 'game': 'position',
                                                     'x': self.map.lastPlayedPos['x'],
                                                     'z': self.map.lastPlayedPos['y'] }))
                playerTurn.played = False
                if self.map.isWin(playerTurn):
                    await updateParty(playerTurn, otherPlayer)
                    await self.broadcast({ 'game': 'end',
                                           'winner': playerTurn.username ,})
                    return
                if self.map.isFull():
                    await self.broadcast({ 'game': 'end',
                                           'winner': 'draw' })
                    return
                self.turn = 'X' if self.turn == 'O' else 'O'
                sended = False
            await asyncio.sleep(0.1)
    
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
                asyncio.create_task(duo.gameLoop()) #a utiliser pour lancer le jeu
            elif len(duo.players) == 0:
                self.remove(duo)

ticTakToe = Game()

def assignPawn(duo: Duo):
    if duo.isXadded == False:
        duo.isXadded = True
        return 'X'
    return 'O'

def assignDuo(message: dict, socket: AsyncWebsocketConsumer):
    duo = ticTakToe.getDuo(message['id'])
    if duo == None:
        duo = Duo(message['id'])
    user = socket.scope['user']
    player = Player(user.username, assignPawn(duo), socket)
    duo.append(player)
    ticTakToe.append(duo)
    return { 'game': 'starting',
             'pawn': player.pawn } 

def leaveDuo(message: dict, socket: AsyncWebsocketConsumer):
    duo = ticTakToe.getDuo(message['id'])
    if duo != None:
        user = socket.scope['user']
        player = duo.getPlayer(user.username)
        if player != None:
            player.disconected = True
    return None

def position(message: dict, socket: AsyncWebsocketConsumer):
    duo = ticTakToe.getDuo(message['id'])
    user = socket.scope['user']
    player = duo.getPlayer(user.username)
    if duo.map.getMapCase(message['x'], message['y']) == '0':
        duo.map.map[message['x']][message['y']] = player.pawn
        duo.map.lastPlayedPos = { 'x': message['x'], 'y': message['y'] }
        player.played = True
    return None

def parseMessage(message: dict, socket: AsyncWebsocketConsumer):
    if 'game' in message:
        if message['game'] == 'starting':
            return assignDuo(message, socket)
        if message['game'] == 'leaved':
            return leaveDuo(message, socket)
        if message['game'] == 'position':
            return position(message, socket)  
    return { 'error': 'Invalid message' }

class TicTacToeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        message = { 'message': 'TicTacToe connection etablished !' }
        await self.send(json.dumps(message))

    async def disconnect(self, close_code):
        await self.close(close_code)

    async def receive(self, text_data):
        message: dict = json.loads(text_data)
        response = parseMessage(message, self)
        if response:
            await self.send(json.dumps(response))