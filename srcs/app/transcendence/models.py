from typing import Any
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, Permission
from django.utils.translation import gettext as _
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    sexe = models.CharField(max_length=64, default='Unknow')
    birthdate = models.DateField(default=timezone.now)
    token = models.CharField(max_length=128)
    avatar = models.ImageField(upload_to='avatars/', default='default_avatar.webp')
    created_at = models.DateTimeField(default=timezone.now)
    last_connexion = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=30, default='Online')
    list_friends = models.ManyToManyField('CustomUser', related_name='friends')
    list_request = models.ManyToManyField('friend_request', related_name='request')
    list_request_sent = models.ManyToManyField('friend_request', related_name='request_sent')
    stat = models.ManyToManyField('Stat_User_by_Game', related_name='stat')
    def __str__(self):
        return self.username

class Game(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30, unique=True)
	description = models.TextField()
	image = models.CharField(max_length=128, default='/var/www/static/default_game.webp')
	genre = models.CharField(max_length=30)
	created_at = models.DateTimeField(auto_now_add=True)
	point_to_win = models.IntegerField(default=10)
	stat = models.ForeignKey('Stat_Game', on_delete=models.CASCADE)
	lobby_game = models.ManyToManyField('Lobby', related_name='lobby')
	tournament = models.ManyToManyField('Tournament', related_name='tournament')
	def __str__(self):
		return self.name

class Stat_Game(models.Model):
	id = models.AutoField(primary_key=True)
	nb_played = models.IntegerField(default=0)
	time_played = models.IntegerField(default=0)
	nb_party = models.IntegerField(default=0)
	id_party = models.ManyToManyField('Party', related_name='party')
	avg_queue_time = models.IntegerField(default=0)
	avg_game_time = models.IntegerField(default=0)
	avg_ratio = models.IntegerField(default=0)

class UserInLobby(models.Model):
	id = models.AutoField(primary_key=True)
	id_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
	id_lobby = models.ForeignKey('Lobby', on_delete=models.CASCADE)
	entry_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.id


class Lobby(models.Model):
	id = models.AutoField(primary_key=True)
	type = models.CharField(max_length=30, default='Public') #sinon Tournoir
	id_game = models.ForeignKey('Game', on_delete=models.CASCADE)
	user = models.ManyToManyField('UserInLobby', related_name='user')
	def __str__(self):
		return self.id


class Tournament(models.Model):
	id = models.AutoField(primary_key=True)
	id_game = models.ForeignKey('Game', on_delete=models.CASCADE)
	name = models.CharField(max_length=30, default='Tournament')
	started_at = models.DateTimeField(auto_now_add=True)
	ended_at = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=False)
	winner = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='winner')
	creator = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='creator')
	lobby_tournament = models.ManyToManyField('Lobby', related_name='lobby')
	parties = models.ManyToManyField('Party', related_name='party')
	nb_round = models.IntegerField(default=0)

	

class Party(models.Model):
	id = models.AutoField(primary_key=True)
	id_game = models.ForeignKey('Game', on_delete=models.CASCADE)
	name = models.CharField(max_length=30, default='Party')
	# is_full = models.BooleanField(default=False)
	started_at = models.DateTimeField(auto_now_add=True)
	ended_at = models.DateTimeField(auto_now=True)
	ratio_diff = models.IntegerField(default=0)
	status = models.CharField(max_length=30, default='Waiting')
	player1 = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player1')
	player2 = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player2')
	score1 = models.IntegerField(default=0)
	score2 = models.IntegerField(default=0)
	id_winner = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='winner')
	id_loser = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='loser')
	type = models.CharField(max_length=30, default='Public') #sinon Tournoir
	round_nb = models.IntegerField(default=0)
	id_tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, default=None)
	def __str__(self):
		return self.id

class PartyInTournament(models.Model)
	id = models.AutoField(primary_key=True)
	match = models.ForeignKey('Party', on_delete=models.CASCADE)
	round_nb = models.IntegerField(default=0)
	id_tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, default=None)
	def __str__(self):
		return self.id

class friend_request(models.Model):
	id = models.AutoField(primary_key=True)
	id_sender = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='sender')
	id_receiver = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='receiver')
	created_at = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=30, default='Waiting')
	def __str__(self):
		return self.id


class Stat_User_by_Game(models.Model):
	id = models.AutoField(primary_key=True)
	id_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
	id_game = models.ForeignKey('Game', on_delete=models.CASCADE)
	nb_played = models.IntegerField(default=0)
	time_played = models.IntegerField(default=0)
	nb_win = models.IntegerField(default=0)
	nb_lose = models.IntegerField(default=0)
	win_rate = models.IntegerField(default=0)
	ratio = models.IntegerField(default=0)
