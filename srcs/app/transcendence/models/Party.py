
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
	id_tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		return self.id
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
			'round_nb': self.round_nb,
			'id_tournament': self.id_tournament.id if self.id_tournament else None
	}

