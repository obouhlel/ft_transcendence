from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Game, Tournament, Lobby, PartyInTournament
import json
from django.utils import timezone


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

@login_required
@require_http_methods(['POST'])
def createTournament(request):
	data = json.loads(request.body)
	if 'id_game' not in data:
		return JsonResponse({'status': 'error', 'message': 'You must provide a game id.'}, status=400)
	try:
		game = Game.objects.get(id=data['id_game'])
		tournament = Tournament.objects.create(game=game, user=request.user)
		tournament.name = game.name + ' tournament by ' + request.user.username
		lobby = Lobby.objects.create(type='tournament', id_game=game.id)
		
		lobby.save()
		tournament.lobby_tournament = lobby
		
		tournament.save()
		return JsonResponse({'status': 'ok', 'id_tournament': tournament.id})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
	
#---------------------------------PUT TOURNAMENT---------------------------------#
#another user can join the tournament
@login_required
@require_http_methods(['PUT'])
def joinTournament(request, id_tournament):
	try:
		tournament = Tournament.objects.get(id=id_tournament)
		tournament.user_tournament.add(request.user)
		return JsonResponse({'status': 'ok', 'message': 'You joined the tournament.'})
	except Tournament.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This tournament does not exist.'}, status=404)
	
#when the tournament have enough players, the creator can start the tournament => create lobbies
@login_required
		