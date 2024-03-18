from typing import Any
from django.utils.translation import gettext as _
from django.db import models
from django.utils import timezone
from django.http import JsonResponse
from .Party import Party, PartyInTournament
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Tournament(models.Model):
	id = models.AutoField(primary_key=True)
	game = models.ForeignKey('Game', on_delete=models.CASCADE)
	name = models.CharField(max_length=30, default='Tournament')
	creator = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
	status = models.CharField(max_length=30, default='waiting')
	nb_player_to_start = models.IntegerField(default=4)
	nb_round = models.IntegerField(default=2)
	started_at = models.DateTimeField(auto_now_add=True)
	ended_at = models.DateTimeField(null=True, blank=True)
	users = models.ManyToManyField('CustomUser', related_name='tournaments')
	winner = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, related_name='winner_Tournament')

	@property
	def users_count(self):
		return self.users.count()

	def __str__(self):
		return f"{self.name} tournament {self.id} for {self.game.name} game by {self.creator}"

	def getAllParties(self):
		list_party = self.parties.all()
		party = [party.Party_data() for party in list_party]
		return party

	def getAllUser(self):
		list_user = self.users.all()
		user = [user.user_data(minimal=True) for user in list_user]
		return user

	def getParties(self):
		list_party = self.party_set.all()
		return [party.id for party in list_party]

	def tournament_data(self):
		return {
			'id': self.id,
			'id_game': self.game.id,
			'name': self.name,
			'creator_id': self.creator.id,
			'nb_player_to_start': self.nb_player_to_start,
			'status': self.status, # 'waiting', "playing", "finished"
			'started_at': self.started_at,
			'ended_at': self.ended_at,
			'parties': self.getParties(),
			'nb_round': self.nb_round,
			'users': self.getAllUser(),
			'winner_id': self.winner.id if self.winner else None
	}

	def end_tournament(self):
		self.ended_at = timezone.now()
		self.status = 'Finished'
		last_party = self.partyintournament_set.filter(round_nb=self.nb_round)
		if last_party.count() > 1:
			return JsonResponse({'status': 'error', 'message': _('Something went wrong. Contact Tham')}, status=500)
		elif last_party.count() == 1:
			self.winner_tournament = last_party.party.winner_party
		self.save()
		return JsonResponse({'status': 'ok', 'message': ('Tournament ended successfully.')})

	def make_party_of_round(self, round_nb, list_players):
		if len(list_players) != 2**round_nb:
			return JsonResponse({'status': 'error', 'message': _('The number of players is not correct.')}, status=400)
		for i in range(0, len(list_players), 2):
			party = Party.startParty(list_players[i], list_players[i+1], self.game, "tournament")
			PartyInTournament.objects.create(party=party, tournament=self, round_nb=round_nb, index=i//2)
		return JsonResponse({'status': 'ok', 'message': _('Parties created successfully.')})

	def next_round(self, round_nb):
		if self.partyintournament_set.filter(round_nb=round_nb, party__status='finished').count() != self.partyintournament_set.filter(round_nb=round_nb).count():
			return JsonResponse({'status': 'error', 'message': _('All parties of this round are not finished yet.')}, status=400)
		parties = self.partyintournament_set.filter(round_nb=round_nb)
		winners = []
		for party in parties:
			winners.append(party.party.winner_party)
		if len(winners) == 1:
			self.winner_tournament = winners[0]
			self.end_tournament()
		else:
			self.make_party_of_rounb(round_nb+1, winners)
		return JsonResponse({'status': 'ok', 'message': ('Next round started successfully.')})

