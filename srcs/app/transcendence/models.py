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
	status = models.CharField(max_length=30, default='Online')
	list_friends = models.ManyToManyField('CustomUser', related_name='friends')
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
			'friends_received': self.getFriendRequestReceived(),
			'request_sent': self.getFriendRequestSent(),
			'list_friends': self.friend_user_data(),
			'stat': self.getStat()
		}
	def friend_user_data(self):
		data = []
		list_friends = self.list_friends.all()
		for friend in list_friends:
			data += friend.user_data()
		return data
	def getFriendRequestReceived(self):
		list_friend_request = self.friend_request_set.all().filter(receiver=self)
		data = []
		for re in list_friend_request:
			data += re.friend_request_data()
		return data
	def getFriendRequestSent(self):
		list_friend_request = self.friend_request_set.all().filter(sender=self)
		data = []
		for re in list_friend_request:
			data += re.friend_request_data()
		return data
	def getStat(self):
		list_stat = self.stat.all()
		stat = [stat.stat_user_by_game_data() for stat in list_stat]
		return stat
	def get_notifications(self):
		list_notification = self.notification_set.all()
		notification = [notification.notification_data() for notification in list_notification]
		return notification

class friend_request(models.Model):
	id = models.AutoField(primary_key=True)
	sender = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='sender')
	receiver = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='receiver')
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.receiver.username + ' received a friend request from ' + self.sender.username
	def friend_request_data(self):
		return {
			'id': self.id,
			'id_sender': self.id_sender,
			'id_receiver': self.id_receiver,
			'created_at': self.created_at,
	}

#----------notifications
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
class Notification(models.Model):
	id = models.AutoField(primary_key=True)
	message = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	is_read = models.BooleanField(default=False)
	user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
	# def __str__(self):
	# 	return self.id
	def send_notification(self):
		self.is_read = False
		self.save()
	def notification_data(self):
		return {
			'id': self.id,
			'message': self.message,
			'created_at': self.created_at,
			'is_read': self.is_read,
			'user': self.user.id
	}
	def send_to_all(self, message: str):
		channel_layer = get_channel_layer()
		async_to_sync(channel_layer.group_send)(
			"public_room",
			{
				"type": "send_notification",
				"message": message
			}
		)


class Game(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30, unique=True)
	description = models.TextField()
	image = models.CharField(max_length=128, default='/var/www/static/default_game.webp')
	genre = models.CharField(max_length=30)
	created_at = models.DateTimeField(auto_now_add=True)
	point_to_win = models.IntegerField(default=10)
	stat = models.OneToOneField('Stat_Game', on_delete=models.CASCADE, related_name='stat')
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
			'stat': self.getStat(),
			'lobby': self.getLobby(),
			'tournament': self.getTournament()
		}
	def getLobby(self):
		list_lobby = self.lobby_set.all()
		lobby = [lobby.lobby_data() for lobby in list_lobby]
		return lobby
	def getParties(self):
		list_party = self.party_set.all()
		party = [party.party_data() for party in list_party]
		return party
	def getTournament(self):
		list_tournament = self.tournament_set.all()
		tournament = [tournament.Tournament_data() for tournament in list_tournament]
		return tournament
	def getStat(self):
		stat = self.stat.stat_game_data()
		return stat

class Stat_Game(models.Model):
	id = models.AutoField(primary_key=True)
	nb_played = models.IntegerField(default=0)
	time_played = models.IntegerField(default=0)
	nb_party = models.IntegerField(default=0)
	avg_game_time = models.IntegerField(default=0)
	# def __str__(self):
	# 	return self.id
	def update(self, time: int):
		self.nb_played += 1
		self.time_played += time
		self.avg_game_time = self.time_played / self.nb_party
		self.save()
	def getPaties(self):
		list_party = self.id_party.all()
		party = [party.Party_data() for party in list_party]
		return party
	def stat_game_data(self):
		return {
			'nb_played': self.nb_played,
			'time_played': self.time_played,
			'nb_party': self.nb_party,
			'avg_game_time': self.avg_game_time,
			'parties': self.Game.getParties()
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
	# def __str__(self):
	# 	return self.id
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
	game = models.ForeignKey('Game', on_delete=models.CASCADE)
	user = models.ManyToManyField('CustomUser', through='UserInLobby', through_fields=('id_lobby', 'id_user'))
	tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, blank=True)
	# def __str__(self):
	# 	return self.id
	def getAllUser(self):
		list_user = self.user.all()
		user = [user.UserInLobby_data() for user in list_user]
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


class Tournament(models.Model):
	id = models.AutoField(primary_key=True)
	game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='game')
	name = models.CharField(max_length=30, default='Tournament')
	creator = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='creator')
	status = models.CharField(max_length=30, default='Waiting')
	nb_player_to_start = models.IntegerField(default=4)
	nb_round = models.IntegerField(default=2)
	started_at = models.DateTimeField(auto_now_add=True)
	ended_at = models.DateTimeField(auto_now=True)
	# is_active = models.BooleanField(default=False)
	user_tournament = models.ManyToManyField('CustomUser', related_name='user')
	invited_user = models.ManyToManyField('CustomUser', related_name='invited')
	winner_Tournament = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='winner_Tournament')
	
	# def __str__(self):
	# 	return self.id
	def getAllParties(self):
		list_party = self.parties.all()
		party = [party.Party_data() for party in list_party]
		return party
	def getAllUser(self):
		list_user = self.user_tournament.all()
		user = [user.user_data() for user in list_user]
		return user
	def getAllInvitedUser(self):
		list_user = self.invited_user.all()
		user = [user.user_data() for user in list_user]
		return user
	def Tournament_data(self):
		return {
			'id': self.id,
			'id_game': self.id_game,
			'name': self.name,
			'creator': self.creator,
			'nb_player_to_start': self.nb_player_to_start,
			'status': self.status, # 'Waiting', "Playing", "Finished"
			'started_at': self.started_at,
			'ended_at': self.ended_at,
			# 'is_active': self.is_active,
			# 'lobby_tournament': self.lobby_set.all().first().id if self.lobby_set.all().first() else None,
			# 'parties': self.parties,
			'nb_round': self.nb_round,
			'user_tournament': self.getAllUser(),
			'invited_user': self.getAllInvitedUser(),
			'winner': self.winner,
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
	tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, blank=True)
	# def __str__(self):
	# 	return self.id
	def __init__(self, *args: Any, **kwargs: Any) -> None:
		super().__init__(*args, **kwargs)
	def update_end(self):
		self.ended_at = timezone.now()
		self.status = 'Ended'
		if self.score1 > self.score2:
			self.winner_party = self.player1
			self.loser_party = self.player2
		else:
			self.winner_party = self.player2
			self.loser_party = self.player1
		self.time_played = (self.ended_at - self.started_at).seconds
		self.save()
	def party_data(self):
		return {
			'id': self.id,
			'id_game': self.id_game.id,
			'name': self.name,
			'started_at': self.started_at,
			'ended_at': self.ended_at,
			'time_played': self.time_played,
			'status': self.status,
			'player1': self.player1.id,
			'player2': self.player2.id,
			'score1': self.score1,
			'score2': self.score2,
			'winner_party': self.winner_party.id if self.winner_party else None,
			'loser_party': self.loser_party.id if self.loser_party else None,
			'type': self.type,
			'round_nb': self.round_nb,
			'id_tournament': self.id_tournament.id if self.id_tournament else None
	}
