from typing import Any
from django.utils.translation import gettext as _
from django.db import models

class Lobby(models.Model):
	id = models.AutoField(primary_key=True)
	game = models.OneToOneField("Game", on_delete=models.CASCADE)
	users = models.ManyToManyField('CustomUser', through='UserInLobby', through_fields=('lobby', 'user'))
	def __str__(self):
		return f"lobby {self.id} for {self.game.name}"
	def getAllUser(self):
		list_user = self.users.all()
		user = [user.id for user in list_user]
		return user
	def lobby_data(self):
		return {
			'id': self.id,
			# 'type': self.type,
			# 'game': self.game.id,
			'user': self.getAllUser()
	}

#a user can be in one and only one lobby
class UserInLobby(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
	lobby = models.ForeignKey('Lobby', on_delete=models.CASCADE)
	entry_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.user.id} in lobby {self.lobby.id} since {self.entry_at}"
	def UserInLobby_data(self):
		return {
			'id': self.id,
			'user': self.user.id,
			'lobby': self.lobby.id,
			'entry_at': self.entry_at
	}
