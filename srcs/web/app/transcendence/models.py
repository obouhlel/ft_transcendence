from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, Permission
from django.utils.translation import gettext as _
from django.db import models
from django.utils import timezone


# abstractUser has the following fields:
# username, first_name, last_name, email
# password  groups  user_permissions is_staff is_active
# is_superuser last_login date_joined
# You can add more fields to the user model by creating a custom model that inherits from AbstractUser. 

class CustomUser(AbstractUser):
	sex = models.CharField(max_length=1, default='N')
	birthday = models.DateField(default=timezone.now)
	token = models.CharField(max_length=128)
	avatar = models.CharField(max_length=128, default='/var/www/static/default_avatar.webp')
	created_at = models.DateTimeField(auto_now_add=True)
	last_connexion = models.DateTimeField(auto_now=True)
	list_friends = models.ManyToManyField('CustomUser', related_name='friends')
	list_blocked = models.ManyToManyField('CustomUser', related_name='blocked')
	list_request = models.ManyToManyField('friend_request', related_name='request')
	list_request_sent = models.ManyToManyField('Friend_request', related_name='request_sent')
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
	# updated_at = models.DateTimeField(auto_now=True)
	stat = models.ForeignKey('Stat_Game', on_delete=models.CASCADE)
	def __str__(self):
		return self.name

class Stat_Game(models.Model):
	id = models.AutoField(primary_key=True)
	nb_played = models.IntegerField(default=0)
	time_played = models.IntegerField(default=0)
	nb_party = models.IntegerField(default=0)


class Party(models.Model):
	id = models.AutoField(primary_key=True)
	id_game = models.ForeignKey('Game', on_delete=models.CASCADE)
	name = models.CharField(max_length=30, default='Party')
	is_full = models.BooleanField(default=False)
	started_at = models.DateTimeField(auto_now_add=True)
	ended_at = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=30, default='Waiting')
	player1 = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player1')
	player2 = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player2')
	id_winner = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='winner')
	id_loser = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='loser')
	def __str__(self):
		return self.id

class Friend_request(models.Model):
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
	def __str__(self):
		return self.id
