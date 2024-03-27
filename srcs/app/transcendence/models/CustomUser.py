import os
import uuid
from typing import Any
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.db import models
from django.utils import timezone
from .Game import Game

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('avatars/', filename)

# AbstractUser has the following fields:
# - username
# - first_name
# - last_name
# - email
# - password
# - groups
# - user_permissions
# - is_staff
# - is_active
# - is_superuser
# - last_login
# - date_joined

import logging
logger = logging.getLogger(__name__)	

class CustomUser(AbstractUser):
	alias = models.CharField(max_length=30)
	avatar = models.ImageField(upload_to=get_file_path, default='avatars/default_avatar.png')
	status = models.CharField(max_length=30, default='Offline')
	list_friends = models.ManyToManyField('self')
	birthdate = models.DateField(default=timezone.now)
	sexe = models.CharField(max_length=1, default='U')
	token = models.CharField(max_length=128)

	def __str__(self):
		return f"{self.username}"

	def update_status(self, status: str):
		self.status = status
		self.save(update_fields=['status']) #fix avatar update

	def update_last_connexion(self):
		self.last_connexion = timezone.now()
		self.save(update_fields=['last_connexion'])

	def user_data(self, minimal: bool = False):
		if minimal:
			return {
				'id': self.id,
				'username': self.username,
				'alias': self.alias,
				'avatar': self.avatar.url if self.avatar else None,
				'status': self.status,
			}
		return {
			'id': self.id,
			'email': self.email,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'username': self.username,
			'alias': self.alias,
			'avatar': self.avatar.url if self.avatar else None,
			'is_active': self.is_active,
			'is_superuser': self.is_superuser,
			'last_login': self.last_login,
			'date_joined': self.date_joined,
			'sexe': self.sexe,
			'birthdate': self.birthdate,
			'status': self.status,
			'list_friends': self.getFriends(),
			'friends_received': self.getFriendRequestReceived(),
			'request_sent': self.getFriendRequestSent(),
			'stat': self.getStat()
		}

	def getFriends(self):
		list_friends = self.list_friends.all()
		return [friend.user_data(minimal=True) for friend in list_friends]

	def getFriendRequestReceived(self):
		list_friend_request = self.receiver.all()
		return [re.friend_request_data() for re in list_friend_request]

	def getFriendRequestSent(self):
		list_friend_request = self.sender.all()
		return [re.friend_request_data() for re in list_friend_request]

	def getStat(self):
		list_stat = self.stats.all()
		return [stat.stat_user_by_game_data() for stat in list_stat]
	def joinLobby(self, game_id: int):
		game = Game.objects.get(id=game_id)
		lobby = game.lobby
		if self in lobby.users.all():
			return game_id
		if self.lobby_set.count() > 0:
			return None
		lobby.users.add(self)
		return game_id
	def leaveLobby(self, game_id: int):
		game = Game.objects.get(id=game_id)
		lobby = game.lobby
		if self not in lobby.users.all():
			return None
		lobby.users.remove(self)
		return game_id
	def updateStat(self, game_id: int, time: int, win: bool, draw: bool = False):
		game = Game.objects.get(id=game_id)
		stat = self.stats.get(game=game)
		stat.update(time, win, draw)
		return game_id
	

class FriendRequest(models.Model):
	id = models.AutoField(primary_key=True)
	sender = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='sender')
	receiver = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='receiver')
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"{self.sender} send friend request to {self.receiver}"
	
	def friend_request_data(self):
		return {
			'id': self.id,
			'sender': {
				'username': self.sender.username,
				'avatar': self.sender.avatar.url if self.sender.avatar else None,
			},
			'receiver': self.receiver.id,
			'message': f"You have a friend request from {self.sender.username}",
			'created_at': self.created_at,
		}