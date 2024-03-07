from typing import Any
from django.utils.translation import gettext as _
from django.db import models


class Game(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30, unique=True)
	description = models.TextField()
	image = models.CharField(max_length=128, default='/var/www/static/default_game.webp')
	genre = models.CharField(max_length=80)
	created_at = models.DateTimeField(auto_now_add=True)
	point_to_win = models.IntegerField(default=10)
	def __str__(self):
		return f"{self.name} game {self.id}"
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
		list_party = self.party_set.filter(status='Finished').order_by('-ended_at')[:5]
		# list_party = self.party_set.all()
		party = [party.party_data() for party in list_party]
		return party
	def getTournament(self):
		list_tournament = self.tournament_set.all()
		tournament = [tournament.tournament_data() for tournament in list_tournament]
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
	game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='stat')
	def __str__(self):
		return f"stat for {self.game} game {self.id}"
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
			'parties': self.game.getParties()
		}

