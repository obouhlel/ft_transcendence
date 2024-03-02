from typing import Any
from django.utils.translation import gettext as _
from django.db import models


class Lobby(models.Model):
	id = models.AutoField(primary_key=True)
	type = models.CharField(max_length=30, default='Public') #sinon Tournoir
	game = models.ForeignKey('Game', on_delete=models.CASCADE)
	user = models.ManyToManyField('CustomUser', through='UserInLobby', through_fields=('id_lobby', 'id_user'))
	tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, blank=True)
	# def __str__(self):
	# 	return self.id
	def getAllUser(self):
		list_user = self.user.all()
		user = [user.id for user in list_user]
		return user
	def lobby_data(self):
		return {
			'id': self.id,
			'type': self.type,
			'id_game': self.game.id,
			'user': self.getAllUser()
	}

#a user can be in one and only one lobby
class UserInLobby(models.Model):
	id = models.AutoField(primary_key=True)
	id_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
	id_lobby = models.ForeignKey('Lobby', on_delete=models.CASCADE)
	entry_at = models.DateTimeField(auto_now_add=True)
	# def __str__(self):
	# 	return self.id
	def UserInLobby_data(self):
		return {
			'id': self.id,
			'id_user': self.id_user,
			'id_lobby': self.id_lobby,
			'entry_at': self.entry_at
	}
