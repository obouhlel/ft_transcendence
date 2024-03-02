from typing import Any
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, Permission
from django.utils.translation import gettext as _
from django.db import models
from django.utils import timezone


#AbstractUser has the following fields: username, first_name, last_name, email, password, groups, user_permissions, is_staff, is_active, is_superuser, last_login, date_joined
class CustomUser(AbstractUser):
	is_admin = models.BooleanField(default=False)
	sexe = models.CharField(max_length=64, default='Unknow')
	birthdate = models.DateField(default=timezone.now)
	token = models.CharField(max_length=128)
	# avatar = models.ImageField(upload_to='avatars/', default='default_avatar.webp')
	avatar = models.ImageField(upload_to='avatars/')
	created_at = models.DateTimeField(default=timezone.now)
	last_connexion = models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length=30, default='offline')
	list_friends = models.ManyToManyField('CustomUser', related_name='friends')
	list_request = models.ManyToManyField('friend_request', related_name='request')
	list_request_sent = models.ManyToManyField('friend_request', related_name='request_sent')
	stat = models.ManyToManyField('Stat_User_by_Game', related_name='stat')
	def __str__(self):
		return self.username
	def update_status(self, status: str):
		self.status = status
		self.save()
	def update_last_connexion(self):
		self.last_connexion = timezone.now()
		self.save()
	def update_avatar(self, avatar: str):
		self.avatar = avatar
		self.save()
	def user_data(self):
		return {
			'id': self.id,
			'email': self.email,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'is_active': self.is_active,
			'is_superuser': self.is_superuser,
			'last_login': self.last_login,
			'date_joined': self.date_joined,
			'username': self.username,
			'is_admin': self.is_admin,
			'sexe': self.sexe,
			'birthdate': self.birthdate,
			'avatar': self.avatar.path if self.avatar else None,
			'created_at': self.created_at,
			'last_connexion': self.last_connexion,
			'status': self.status,
			# 'list_friends': self.list_friends,
			# 'list_request': self.list_request,
			# 'list_request_sent': self.list_request_sent,
			# 'stat': self.stat
		}
	def friend_data(self):
		list_friends = [user.user_data() for user in self.list_friends.all()]
		for user in list_friends:
			data += [user.user_data()]
		return data


class Game(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30, unique=True)
	description = models.TextField()
	image = models.CharField(max_length=128, default='img/default_game.jpg')
	genre = models.CharField(max_length=30)
	created_at = models.DateTimeField(auto_now_add=True)
	point_to_win = models.IntegerField(default=10)
	stat = models.ForeignKey('Stat_Game', on_delete=models.CASCADE)
	lobby_game = models.ManyToManyField('Lobby', related_name='lobby')
	tournament = models.ManyToManyField('Tournament', related_name='tournament')
	def __str__(self):
		return self.name
	def game_data(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'image': self.image,
			'genre': self.genre,
			'created_at': self.created_at,
			'point_to_win': self.point_to_win,
			# 'stat': self.stat,
			# 'lobby_game': self.lobby_game,
			# 'tournament': self.tournament
		}

class Stat_Game(models.Model):
	id = models.AutoField(primary_key=True)
	nb_played = models.IntegerField(default=0)
	time_played = models.IntegerField(default=0)
	nb_party = models.IntegerField(default=0)
	id_party = models.ManyToManyField('Party', related_name='id_party')
	avg_game_time = models.IntegerField(default=0)
	def __str__(self):
		return self.id
	def update(self, time: int, Party_id: int):
		self.nb_played += 1
		self.time_played += time
		self.avg_game_time = self.time_played / self.nb_party
		self.save()
	def stat_game_data(self):
		return {
			'nb_played': self.nb_played,
			'time_played': self.time_played,
			'nb_party': self.nb_party,
			'avg_game_time': self.avg_game_time
		}




class Stat_User_by_Game(models.Model):
	id = models.AutoField(primary_key=True)
	id_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
	id_game = models.ForeignKey('Game', on_delete=models.CASCADE)
	nb_played = models.IntegerField(default=0)
	time_played = models.IntegerField(default=0)
	nb_win = models.IntegerField(default=0)
	nb_lose = models.IntegerField(default=0)
	ratio = models.IntegerField(default=0)
	def __str__(self):
		return self.id
	def update(self,time:int, win: bool):
		self.nb_played += 1
		self.time_played += time
		if win:
			self.nb_win += 1
		else:
			self.nb_lose += 1
		self.ratio = self.nb_win / self.nb_played
		self.save()
	def stat_user_by_game_data(self):
		return {
			'id': self.id,
			'id_user': self.id_user,
			'id_game': self.id_game,
			'nb_played': self.nb_played,
			'time_played': self.time_played,
			'nb_win': self.nb_win,
			'nb_lose': self.nb_lose,
			'ratio': self.ratio
	}


class Lobby(models.Model):
	id = models.AutoField(primary_key=True)
	type = models.CharField(max_length=30, default='Public') #sinon Tournoir
	id_game = models.ForeignKey('Game', on_delete=models.CASCADE)
	user = models.ManyToManyField('UserInLobby', related_name='user')
	def __str__(self):
		return self.id
	def Lobby_data(self):
		return {
			'id': self.id,
			'type': self.type,
			'id_game': self.id_game,
			'user': self.user
	}

#a user can be in one and only one lobby
class UserInLobby(models.Model):
	id = models.AutoField(primary_key=True)
	id_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
	id_lobby = models.ForeignKey('Lobby', on_delete=models.CASCADE)
	entry_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.id
	def UserInLobby_data(self):
		return {
			'id': self.id,
			'id_user': self.id_user,
			'id_lobby': self.id_lobby,
			'entry_at': self.entry_at
	}


class Tournament(models.Model):
	id = models.AutoField(primary_key=True)
	id_game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='game')
	name = models.CharField(max_length=30, default='Tournament')
	started_at = models.DateTimeField(auto_now_add=True)
	ended_at = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=False)
	status = models.CharField(max_length=30, default='Waiting')
	winner_Tournament = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='winner_Tournament')
	creator = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='creator')
	lobby_tournament = models.ForeignKey('Lobby', on_delete=models.CASCADE, default=None)
	parties = models.ManyToManyField('Party', related_name='party')
	user_tournament = models.ManyToManyField('CustomUser', related_name='user')
	invited_user = models.ManyToManyField('CustomUser', related_name='invited')
	nb_player_to_start = models.IntegerField(default=4)
	def __str__(self):
		return self.id
	def Tournament_data(self):
		return {
			'id': self.id,
			'id_game': self.id_game,
			'name': self.name,
			'started_at': self.started_at,
			'ended_at': self.ended_at,
			'is_active': self.is_active,
			'winner': self.winner,
			'creator': self.creator,
			'lobby_tournament': self.lobby_tournament,
			'parties': self.parties,
			'nb_round': self.nb_round,
			'user_tournament': self.user_tournament.all(),
			'nb_player': len(self.user_tournament)
	}

	

class Party(models.Model):
	id = models.AutoField(primary_key=True)
	id_game = models.ForeignKey('Game', on_delete=models.CASCADE)
	name = models.CharField(max_length=30, default='Party')
	# is_full = models.BooleanField(default=False)
	started_at = models.DateTimeField(auto_now_add=True)
	ended_at = models.DateTimeField(auto_now=True)
	time_played = models.IntegerField(default=0)
	status = models.CharField(max_length=30, default='Waiting')
	player1 = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player1')
	player2 = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player2')
	score1 = models.IntegerField(default=0)
	score2 = models.IntegerField(default=0)
	winner_party = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='winner_party')
	loser_party = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='loser_party')
	type = models.CharField(max_length=30, default='Public') #sinon Tournoir
	round_nb = models.IntegerField(default=0)
	id_tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, default=None)
	def __str__(self):
		return self.id
	def __init__(self, *args: Any, **kwargs: Any) -> None:
		super().__init__(*args, **kwargs)
	def update_end(self):
		self.ended_at = timezone.now()
		self.status = 'Ended'
		if self.score1 > self.score2:
			self.id_winner = self.player1
			self.id_loser = self.player2
		else:
			self.id_winner = self.player2
			self.id_loser = self.player1
		self.time_played = (self.ended_at - self.started_at).seconds
		self.save()
	def Party_data(self):
		return {
			'id': self.id,
			'id_game': self.id_game,
			'name': self.name,
			'started_at': self.started_at,
			'ended_at': self.ended_at,
			'time_played': self.time_played,
			'status': self.status,
			'player1': self.player1,
			'player2': self.player2,
			'score1': self.score1,
			'score2': self.score2,
			'id_winner': self.id_winner,
			'id_loser': self.id_loser,
			'type': self.type,
			'round_nb': self.round_nb,
			'id_tournament': self.id_tournament
	}

class PartyInTournament(models.Model):
	id = models.AutoField(primary_key=True)
	match = models.ForeignKey('Party', on_delete=models.CASCADE)
	round_nb = models.IntegerField(default=0)
	id_tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, default=None)
	def __str__(self):
		return self.id
	def PartyInTournament_data(self):
		return {
			'id': self.id,
			'match': self.match,
			'round_nb': self.round_nb,
			'id_tournament': self.id_tournament
	}

class friend_request(models.Model):
	id = models.AutoField(primary_key=True)
	id_sender = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='sender')
	id_receiver = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='receiver')
	created_at = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=30, default='Waiting')
	def __str__(self):
		return self.id
	def friend_request_data(self):
		return {
			'id': self.id,
			'id_sender': self.id_sender,
			'id_receiver': self.id_receiver,
			'created_at': self.created_at,
			'status': self.status
	}
