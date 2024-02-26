
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from transcendence.models  import Party, Game, CustomUser, Stat_Game, Stat_User_by_Game 
import json
from django.utils import timezone

#CRUD : Create, Read, Update, Delete
#Create: POST
#Read: GET
#Update: PUT
#Delete: DELETE


#---------------------------------GET PARTY---------------------------------#
@login_required
@require_http_methods(['GET'])
def getPartyById(request, id):
	try:
		party = Party.objects.get(id=id)
		data = party.party_data()
		return JsonResponse({'status': 'ok', 'party': data})
	except Party.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This party does not exist.'}, status=404)

@login_required
@require_http_methods(['GET'])
def getAllParties(request):
	parties = Party.objects.all()
	data = []
	for party in parties:
		data += [party.party_data()]
	return JsonResponse({'status': 'ok', 'parties': data})

@login_required
@require_http_methods(['GET'])
def getPartyByGame(request, id_game):
	try:
		game = Game.objects.get(id=id_game)
		parties = game.party_game.all()
		data = [party.party_data() for party in parties]
		return JsonResponse({'status': 'ok', 'parties': data})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
	except Party.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This party does not exist.'}, status=404)


@login_required
@require_http_methods(['GET'])
def getUserInParty(request, id_party):
	try:
		party = Party.objects.get(id=id_party)
		users = [party.player1, party.player2]
		data = [user.user_data() for user in users]
		return JsonResponse({'status': 'ok', 'party': data})
	except Party.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This party does not exist.'}, status=404)




# -------------------------------POST PARTY-----------------------------#
@login_required
@require_http_methods(['POST'])
def createParty(request):
	data = json.loads(request.body)
	id_game = data['id_game']
	id_user1 = data['id_user1']
	id_user2 = data['id_user2']
	try:
		game = Game.objects.get(id=id_game)
		user1 = CustomUser.objects.get(id=id_user1)
		user2 = CustomUser.objects.get(id=id_user2)
		party = Party.objects.create(id_game=game, player1=user1, player2=user2,
							   started_at=timezone.now())
		return JsonResponse({'status': 'ok', 'message': 'Party created successfully.'})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)

@login_required
@require_http_methods(['POST'])
def addUserToParty(request, id_party):
	data = json.loads(request.body)
	id_party = data['id_party']
	id_user = data['id_user']
	try:
		party = Party.objects.get(id=id_party)
		user = CustomUser.objects.get(id=id_user)
		party.player2 = user
		party.save()
		return JsonResponse({'status': 'ok', 'message': 'User added successfully.'})
	except Party.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This party does not exist.'}, status=404)
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)
	

def isUserInParty(party, user):
	if party.player1 == user or party.player2 == user:
		return True
	else:
		return False
		

def EndParty(party):
	party.update_end()
	try:
		stat_game = Stat_Game.objects.get(id_game=party.id_game)
		stat_game.update(party.time_played, party.id)
		stat_user = Stat_User_by_Game.objects.get(id_user=party.player1, id_game=party.id_game)
		stat_user.update(party.time_played, party.id)
		stat_user = Stat_User_by_Game.objects.get(id_user=party.player2, id_game=party.id_game)
		stat_user.update(party.time_played, party.id)
		#if this party is for tournament, we need to update the tournament
		# if (party.type = "tournament"):
		# 	tournament = party.tournament_party
		# 	checktoNextRound(tournament)
	except Stat_Game.DoesNotExist:
		stat_game = Stat_Game.objects.create(id_game=party.id_game, nb_played=1, time_played=party.time_played, nb_party=1)
		stat_game.save()

@login_required
@require_http_methods(['POST'])
def addPointToParty(request, id_party):
	data = json.loads(request.body)
	id_party = data['id_party']
	id_user = request.user.id
	try:
		party = Party.objects.get(id=id_party)
		user = CustomUser.objects.get(id=id_user)
		if isUserInParty(party, user):
			if party.player1 == user:
				party.score1 += 1
			else:
				party.score2 += 1
			party.save()
			if party.score1 == party.id_game.point_to_win or party.score2 == party.id_game.point_to_win:
				EndParty(party)
				return JsonResponse({'status': 'ok', 'message': 'Party ended successfully.'})
			return JsonResponse({'status': 'ok', 'message': 'Point added successfully.'})
		else:
			return JsonResponse({'status': 'error', 'message': 'You are not in this party.'}, status=400)
	except Party.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This party does not exist.'}, status=404)
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)


