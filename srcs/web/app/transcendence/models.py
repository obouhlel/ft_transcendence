from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, Permission
from django.utils.translation import gettext as _
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    # Ajoutez vos champs personnalisés ici
    sexe = models.CharField(max_length=50)
    birthdate = models.DateField()
    token = models.CharField(max_length=50, null=True)
    avatar = models.CharField(max_length=255, default='/var/www/default_avatar.webp')
    status = models.CharField(max_length=50, default='offline')
    id_list_friend = models.ForeignKey('ListFriends', on_delete=models.CASCADE, null=True)

class Game(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=255, default='/var/www/default_game.webp')
    description = models.CharField(max_length=1024)
    genre = models.CharField(max_length=50, null=True)

class StatsGame(models.Model):
    nb_player = models.IntegerField()
    time_played = models.IntegerField()
    nb_party = models.IntegerField()
    id_game = models.ForeignKey(Game, on_delete=models.CASCADE)

class Party(models.Model):
    name = models.CharField(max_length=50)
    is_full = models.BooleanField(default=False)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    status = models.CharField(max_length=50, default='waiting')
    score = models.IntegerField()
    id_game = models.ForeignKey(Game, on_delete=models.CASCADE)
    id_user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user1')
    id_user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user2')
    id_winner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='winner')
    id_looser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='looser')

class ListFriends(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    id_friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friend')

class StatsUserByGame(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_game = models.ForeignKey(Game, on_delete=models.CASCADE)
    time_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    looses = models.IntegerField(default=0)
    nb_played = models.IntegerField(default=0)
