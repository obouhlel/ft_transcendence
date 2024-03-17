from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from transcendence.models  import Game, Tournament, Lobby, CustomUser, Party, PartyInTournament
import json
from django.utils import timezone
import math
import random


#CRUD : Create, Read, Update, Delete
#Create: POST : Create a new tournament with multiple lobbies with a round number
#Read: GET : Get a tournament information by id or by game, get all tournaments
#get all lobbies in a tournament, get all users in a tournament
#Update: PUT : Update a tournament information, add a lobby to a tournament, delete a lobby from a tournament
#Delete: DELETE : Delete a tournament,

#---------------------------------GET TOURNAMENT---------------------------------#
@login_required
@require_http_methods(['GET'])
def getTournamentById(request, id):
	try:
		tournament = Tournament.objects.get(id=id)
		data = tournament.tournament_data()
		return JsonResponse({'status': 'ok', 'tournament': data})
	except Tournament.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This tournament does not exist.'}, status=404)
	
@login_required
@require_http_methods(['GET'])
def getAllTournaments(request):
	tournaments = Tournament.objects.all()
	data = []
	for tournament in tournaments:
		data += [tournament.tournament_data()]
	return JsonResponse({'status': 'ok', 'tournaments': data})

@login_required
@require_http_methods(['GET'])
def getTournamentByGame(request, id_game):
	try:
		game = Game.objects.get(id=id_game)
		tournaments = game.tournament_game.all()
		data = [tournament.tournament_data() for tournament in tournaments]
		return JsonResponse({'status': 'ok', 'tournaments': data})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
	except Tournament.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This tournament does not exist.'}, status=404)
	
@login_required
@require_http_methods(['GET'])
def getLobbyInTournament(request, id_tournament):
	try:
		tournament = Tournament.objects.get(id=id_tournament)
		lobby = tournament.lobby_tournament
		data = lobby.PartyInTournament_data()
		return JsonResponse({'status': 'ok', 'lobby': data})
	except Tournament.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This tournament does not exist.'}, status=404)
	except Lobby.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This lobby does not exist.'}, status=404)
	
@login_required
@require_http_methods(['GET'])
def getUsersInTournament(request, id_tournament):
	try:
		tournament = Tournament.objects.get(id=id_tournament)
		users = tournament.user_tournament.all()
		data = [userInTournament.UserInTournament_data() for userInTournament in users]
		return JsonResponse({'status': 'ok', 'tournament': data})
	except Tournament.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This tournament does not exist.'}, status=404)

#---------------------------------POST TOURNAMENT---------------------------------#
#when user clic on create tournament, he must provide the game id
#the server will create a tournament with the game id and the user id,
#defaut name is  "game_name tournament by user_name"
import logging
def is_power_of_two(n):
	if n < 2:
		return False
	return (n & (n - 1)) == 0


@login_required
@require_http_methods(['POST'])
def createTournament(request):
	data = json.loads(request.body)
	nb_player = data['nb_players'] if 'nb_players' in data else 4
	user = request.user
	name = data['name'] if 'name' in data else None
	if not is_power_of_two(nb_player):
		return JsonResponse({'status': 'error', 'message': 'The number of players must be a power of 2(2,4,8,16...).'}, status=400)
	if 'id_game' not in data:
		return JsonResponse({'status': 'error', 'message': 'You must provide a game id.'}, status=400)
	# if user.tournaments.filter(status = "waiting").count() > 0:
	# 	return JsonResponse({'status': 'error', 'message': 'You are already in another tournament.'}, status=400)
	try:
		game = Game.objects.get(id=data['id_game'])
		tournament = Tournament.objects.create(game=game, nb_player_to_start=nb_player, creator = user)
		tournament.nb_round = math.log2(nb_player)
		tournament.status = 'waiting'
		tournament.start_date = timezone.now()
		tournament.name = name if name else f"{game.name} tournament by {user.username}"
		tournament.users.add(user)
		tournament.save()
		return JsonResponse({'status': 'ok', 'id_tournament': tournament.id})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)



#another user can join the tournament
@login_required
@require_http_methods(['POST'])
def joinTournament(request):
	id_tournament = json.loads(request.body)['id_tournament']
	try:
		tournament = Tournament.objects.get(id=id_tournament)
		user = request.user
		if user.tournaments.filter(status = "waiting").count() > 0:
			return JsonResponse({'status': 'error', 'message': 'ERROR: CAN NOT BE IN MULTIPLE TOURNAMENT AT THE SAME TIME'}, status=400)
		# if (user.tournaments.filter(id=id_tournament)):
		# 	return JsonResponse({'status': 'error', 'message': 'You are already in this tournament.'}, status=400)
		if (tournament.status != 'waiting'):
			return JsonResponse({'status': 'error', 'message': 'Tournament is already started or finished.'}, status=400)
		tournament.users.add(user)
		tournament.save()
		# if (tournament.invited_users.filter(id=user.id)):
		# 	tournament.invited_users.remove(user)
		# 	tournament.save()
		if (tournament.users.count() >= tournament.nb_player_to_start):
			# envoie un signal poiur surligner le bouton start
			pass
		return JsonResponse({'status': 'ok', 'message': 'You joined the tournament.'})
	except Tournament.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This tournament does not exist.'}, status=404)
	
#---------------------------------PUT TOURNAMENT---------------------------------#

@login_required
@require_http_methods(['PUT'])
def startTournament(request):
	#create parties in the tournament
	data = json.loads(request.body)
	id_tournament = data['id_tournament']
	try:
		tournament = Tournament.objects.get(id=id_tournament)
		users = tournament.users.all()
		nb_player = users.count()
		if not is_power_of_two(nb_player):
			return JsonResponse({'status': 'error', 'message': 'The number of players must be a power of 2(2,4,8,16...).'}, status=400)
		if (tournament.status != 'waiting'):
			return JsonResponse({'status': 'error', 'message': 'Tournament is already started or finished.'}, status=400)
		# random.shuffle(users)
		tournament.make_party_of_round(1, users) #create the first round, round_nb = 1
			# send notification to the users to join the party: send the party id
		#change the status of the tournament to "playing"
		tournament.status = 'playing'
		tournament.save()
		#send notification to the users to join the tournament: send the tournament id
		return JsonResponse({'status': 'ok', 'message': 'Tournament started.'})
	except Tournament.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This tournament does not exist.'}, status=404)




#invite a user to join the tournament
@login_required
@require_http_methods(['PUT'])
def inviteUserToTournament(request, id_tournament, id_user):
	try:
		tournament = Tournament.objects.get(id=id_tournament)
		user = CustomUser.objects.get(id=id_user)
		if (tournament.status != 'waiting'):
			return JsonResponse({'status': 'error', 'message': 'Tournament is already started or finished.'}, status=400)
		#if user is in another tournament, he can't join
		if (user.tournament_user.all()):
			return JsonResponse({'status': 'error', 'message': 'This user is already in another tournament.'}, status=400)
		if (user in tournament.user_tournament.all()):
			return JsonResponse({'status': 'error', 'message': 'This user is already in the tournament.'}, status=400)
		if (user in tournament.invited_user.all()):
			return JsonResponse({'status': 'error', 'message': 'This user is already invited.'}, status=400)
		tournament.invited_user.add(user)
		tournament.save()
		#send notification to the user to join the tournament: send the tournament id
		return JsonResponse({'status': 'ok', 'message': 'You invited the user to the tournament.'})
	except Tournament.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This tournament does not exist.'}, status=404)
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)


@login_required
@require_http_methods(['POST'])
def leaveTournament(request):
	try:
		id = json.loads(request.body)['id_tournament']
		tournament = Tournament.objects.get(id=id)
		if (request.user not in tournament.users.all()):
			return JsonResponse({'status': 'error', 'message': 'You are not in the tournament.'}, status=400)
		# if (tournament.status != 'waiting'):
		# 	return JsonResponse({'status': 'error', 'message': 'Tournament is already started or finished.'}, status=400)
		tournament.users.remove(request.user)
		tournament.save()
		if (tournament.users.count() == 0):
			tournament.delete()
		return JsonResponse({'status': 'ok', 'message': 'You quit the tournament.'})
	except Tournament.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This tournament does not exist.'}, status=404)

#---------------------------------DELETE TOURNAMENT---------------------------------#
@login_required
@require_http_methods(['DELETE'])
def deleteTournament(request, id_tournament):
	try:
		tournament = Tournament.objects.get(id=id_tournament)
		if (tournament.user != request.user):
			return JsonResponse({'status': 'error', 'message': 'You are not the owner of the tournament.'}, status=400)
		if (tournament.status != 'waiting'):
			return JsonResponse({'status': 'error', 'message': 'Tournament is already started or finished.'}, status=400)
		tournament.delete()
		return JsonResponse({'status': 'ok', 'message': 'Tournament deleted.'})
	except Tournament.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This tournament does not exist.'}, status=404)