
from django.utils.translation import gettext as _
from django.db import models
from django.utils import timezone
from typing import Any


class Party(models.Model):
	id = models.AutoField(primary_key=True)
	game = models.ForeignKey('Game', on_delete=models.CASCADE)
	name = models.CharField(max_length=30, default='Party')
	# is_full = models.BooleanField(default=False)
	started_at = models.DateTimeField(auto_now_add=True)
	ended_at = models.DateTimeField(null=True, blank=True)
	time_played = models.IntegerField(default=0)
	status = models.CharField(max_length=30, default='waiting')
	player1 = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player1')
	player2 = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player2')
	score1 = models.IntegerField(default=0)
	score2 = models.IntegerField(default=0)
	winner_party = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, related_name='winner_party')
	loser_party = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, related_name='loser_party')
	type = models.CharField(max_length=30, default='Matchmaking') #sinon Tournament
	tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, blank=True)
	def __init__(self, *args: Any, **kwargs: Any) -> None:
		super().__init__(*args, **kwargs)
	def __str__(self):
		return f"{self.name} party {self.id} for {self.game} game between {self.player1} and {self.player2}"
	def update_end(self, draw=False):
		self.ended_at = timezone.now()
		self.status = 'finished'
		if self.score1 > self.score2:
			self.winner_party = self.player1
			self.loser_party = self.player2
		elif self.score1 < self.score2:
			self.winner_party = self.player2
			self.loser_party = self.player1
		else:
			self.winner_party = None
			self.loser_party = None
		self.time_played = (self.ended_at - self.started_at).seconds
		self.player1.updateStat(self.game.id, self.time_played, self.winner_party == self.player1, draw)
		self.player2.updateStat(self.game.id, self.time_played, self.winner_party == self.player2, draw)
		self.game.update_stat(self.time_played)
		self.save()
		if self.tournament:
			party_in_tournament = PartyInTournament.objects.get(party=self)
			party_in_tournament.update_end()
	def party_data(self):
		return {
			'id': self.id,
			'id_game': self.game.id,
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
			'id_tournament': self.tournament.id if self.tournament else None
	}
	def startParty(player1, player2, game, type):
		party = Party.objects.create(game=game, player1=player1, player2=player2)
		party.started_at = timezone.now()
		party.type = type
		party.save()
		return party


class PartyInTournament(models.Model):
	id = models.AutoField(primary_key=True)
	party = models.OneToOneField('Party', on_delete=models.CASCADE)
	tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
	round_nb = models.IntegerField(default=0)
	index = models.IntegerField(default=0)
	def __str__(self):
		return f"Party {self.party} in tournament {self.tournament} for round {self.round_nb}"
	def update_end(self):
		if self.index == self.tournament.nb_player_to_start/ (2**self.round_nb): #si c'est le dernier match de la ronde, c'est pas vraiment necessaire
				self.tournament.next_round(self.round_nb)
		self.save()
