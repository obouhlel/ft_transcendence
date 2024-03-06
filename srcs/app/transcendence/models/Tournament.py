from typing import Any
from django.utils.translation import gettext as _
from django.db import models
from django.utils import timezone
from django.http import JsonResponse
from .Party import Party, PartyInTournament



class Tournament(models.Model):
	id = models.AutoField(primary_key=True)
	# game = models.ForeignKey('Game', on_delete=models.CASCADE)
	id_game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='game')
	name = models.CharField(max_length=30, default='Tournament')
	creator = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
	status = models.CharField(max_length=30, default='waiting')
	nb_player_to_start = models.IntegerField(default=4)
	nb_round = models.IntegerField(default=2)
	started_at = models.DateTimeField(auto_now_add=True)
	ended_at = models.DateTimeField(null=True, blank=True)
	# is_active = models.BooleanField(default=False)
	user_tournament = models.ManyToManyField('CustomUser', related_name='user')
	invited_user = models.ManyToManyField('CustomUser', related_name='invited')
	winner_Tournament = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='winner_Tournament')
	def __str__(self):
		return str(self.id)
	def getAllParties(self):
		list_party = self.parties.all()
		party = [party.Party_data() for party in list_party]
		return party
	def getAllUser(self):
		list_user = self.user_tournament.all()
		user = [user.id for user in list_user]
		return user
	def getAllInvitedUser(self):
		list_user = self.invited_user.all()
		user = [user.id for user in list_user]
		return user
	def getParties(self):
		list_party = self.party_set.all()
		return [party.id for party in list_party]
	def tournament_data(self):
		return {
			'id': self.id,
			# 'game_id': self.game.id,
			'id_game': self.id_game,
			'name': self.name,
			'creator_id': self.creator.id,
			'nb_player_to_start': self.nb_player_to_start,
			'status': self.status, # 'waiting', "playing", "finished"
			'started_at': self.started_at,
			'ended_at': self.ended_at,
			# 'is_active': self.is_active,
			# 'lobby_tournament': self.lobby_set.all().first().id if self.lobby_set.all().first() else None,
			'parties': self.getParties(),
			'nb_round': self.nb_round,
			'user_tournament': self.getAllUser(),
			'invited_user': self.getAllInvitedUser(),
			'winner_id': self.winner_Tournament.id if self.winner_Tournament else None
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
		# check if all parties of this round are finished
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

