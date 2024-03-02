from typing import Any
from django.utils.translation import gettext as _
from django.db import models

class Tournament(models.Model):
	id = models.AutoField(primary_key=True)
	game = models.ForeignKey('Game', on_delete=models.CASCADE)
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
			'game_id': self.game.id,
			'name': self.name,
			'creator_id': self.creator.id,
			'nb_player_to_start': self.nb_player_to_start,
			'status': self.status, # 'Waiting', "Playing", "Finished"
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

