from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from transcendence.models  import Lobby, Game, UserInLobby, Party
import json
from django.utils import timezone

#CRUD : Create, Read, Update, Delete
#Create: POST : Create a new lobby
#Read: GET : Get a lobby information by id or by game, get all lobbies
#get all users in a lobby, get all lobby of a game
#Update: PUT : Update a lobby information, add a user to a lobby, delete a user from a lobby
#Delete: DELETE : Delete a lobby, 


#---------------------------------GET LOBBY---------------------------------#

@login_required
@require_http_methods(['GET'])
def getLobbyById(request, id):
	try:
		lobby = Lobby.objects.get(id=id)
		data = lobby.lobby_data()
		return JsonResponse({'status': 'ok', 'lobby': data})
	except Lobby.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This lobby does not exist.'}, status=404)

@login_required
@require_http_methods(['GET'])
def getAllLobbies(request):
	lobbies = Lobby.objects.all()
	data = []
	for lobby in lobbies:
		data += [lobby.lobby_data()]
	return JsonResponse({'status': 'ok', 'lobbies': data})

@login_required
@require_http_methods(['GET'])
def getLobbyByGame(request, id_game):
	try:
		game = Game.objects.get(id=id_game)
		lobbies = game.lobby_game.all()
		data = [lobby.lobby_data() for lobby in lobbies]
		return JsonResponse({'status': 'ok', 'lobbies': data})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
	
@login_required
@require_http_methods(['GET'])
def getUsersInLobby(request, id_lobby):
	try:
		lobby = Lobby.objects.get(id=id_lobby)
		users = lobby.user.all()
		data = [userInLobby.UserInLobby_data() for userInLobby in users]
		return JsonResponse({'status': 'ok', 'lobby': data})
	except Lobby.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This lobby does not exist.'}, status=404)

#a user can be in one and only one lobby
@login_required
@require_http_methods(['GET'])
def getLobbyofUser(request, id_user):
	try:
		user = UserInLobby.objects.get(id_user=id_user)
		data = user.lobby.lobby_data()
		return JsonResponse({'status': 'ok', 'lobby': data})
	except UserInLobby.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user is not in any lobby.'}, status=404)
	
@login_required
@require_http_methods(['GET'])
def getLobbyofGame(request, id_game):
	try:
		game = Game.objects.get(id=id_game)
		lobby = game.lobby_game.all()
		data = [lobby.lobby_data() for lobby in lobby]
		return JsonResponse({'status': 'ok', 'lobby': data})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
	
@login_required
@require_http_methods(['GET'])
def getLobbyofGamebyType(request, id_game, type):
	try:
		game = Game.objects.get(id=id_game)
		lobby = game.lobby_game.filter(type=type)
		data = [lobby.lobby_data() for lobby in lobby]
		return JsonResponse({'status': 'ok', 'lobby': data})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
	
# -------------------------------POST LOBBY-----------------------------#
	
def newLobby(game, type):
	lobby = Lobby.objects.create(game=game, type=type)
	game.lobby_game.add(lobby)
	return lobby

#when User click on Create a lobby,
#it will create a lobby for this game
# method POST
#in request body: id_game, type, name
#return: id_lobby
#not implemented

#when User click on Play button of a game, 
#it will create a lobby if there is no lobby for this game
# method POST or PUT
#in request body: id_game
#return: id_lobby
#create a UserInLobby for the user with entry_at = now
#type = or 'Public' or 'Tournament'
import logging
logger = logging.getLogger(__name__)
@login_required
@require_http_methods(['POST', 'PUT'])
def joinLobby(request):
	data = json.loads(request.body)
	id_game = data['id_game']
	type = data['type'] if 'type' in data else 'Public' #todo: check if type is valid
	try:
		game = Game.objects.get(id=id_game)
		lobby = game.lobby_set.all()
		#if no lobby for this game, create a new lobby
		if len(lobby) == 0:
			lobby = newLobby(game, type)
		#if there is a lobby of given type, join the lobby
		else:
			lobby = lobby.filter(type=type)
			if len(lobby) == 0:
				lobby = newLobby(game, type)
			else:
				lobby = lobby[0]
		user = request.user
		if (UserInLobby.objects.filter(id_user=user, id_lobby=lobby).count() > 0):
			return JsonResponse({'status': 'ok', 'id_lobby': lobby.id})
		UserInLobby.objects.create(id_user=user, id_lobby=lobby)
		return JsonResponse({'status': 'ok', 'id_lobby': lobby.id})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
	

#when User click on Quit the waiting room,
#it will delete the UserInLobby for the user
# method POST
#in request body: id_lobby
@login_required
@require_http_methods(['POST'])
def quitLobby(request):
	data = json.loads(request.body)
	id_lobby = data['id_lobby']
	try:
		lobby = Lobby.objects.get(id=id_lobby)
		userInLobby = UserInLobby.objects.filter(id_user=request.user, id_lobby=lobby).first()
		if userInLobby:
			userInLobby.delete()
			return JsonResponse({'status': 'ok', 'message': 'You have left the lobby.'})
		else:
			return JsonResponse({'status': 'error', 'message': 'You are not in this lobby.'}, status=400)
	except Lobby.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This lobby does not exist.'}, status=404)




# def find_user_with_most_compatible_ratio(users, current_user):
# 	if len(users) == 0:
# 		return None
# 	compatible = None
# 	current_user_stat = current_user.stat
# 	ratio = 0
# 	for user in users:
# 		if user != current_user:
# 			user_stat = user.stat
# 			if compatible == None:
# 				compatible = user
# 			else:
# 				ratio = abs(user_stat.nb_win/user_stat.nb_played - current_user_stat.nb_win/current_user_stat.nb_played)

	

def find_compatibles_users(users, current_user):
	compatible = None
	now = timezone.now()
	waiting_time = now - current_user.entry_at
	#example: if the player wait for 1 second, the tolerance is 10%
	#if the player wait for 2 seconds, the tolerance is 20%
	#if the player wait for 3 seconds, the tolerance is 30%

	toleance =  waiting_time.seconds / 10
	current_user_stat = current_user.stat
	if current_user_stat.nb_played == 0:
		current_user_ratio = 0
	else:
		current_user_ratio = current_user_stat.nb_win/current_user_stat.nb_played
	#find the most compatible users with the acceptable tolerance
	for user in users:
		if user != current_user:
			user_stat = user.stat
			if user_stat.nb_played == 0:
				user_ratio = 0
			else:
				user_ratio = user_stat.nb_win/user_stat.nb_played
			if compatible == None:
				compatible = user
			else:
				ratio = abs(user_ratio - current_user_ratio)
				if ratio < toleance:
					compatible = user
					return compatible
		else:
			pass
	#how to prevent the user to wait for too long
	#this is not really necessaire
	# if compatible == None and waiting_time.seconds > 30:
	# 	compatible = find_user_with_most_compatible_ratio(users, current_user)
	return compatible

#after joining the lobby, if client receive a id_lobby,
#it will make a request to find a compatible user every 2 seconds
# method POST
#in request body: id_lobby
#return: id_party
#if return id_party, it will create a party with the user and the user found
#and delete the UserInLobby for the user
#if return nothing, it will continue to wait

@login_required
@require_http_methods(['POST'])
def findCompatiblesUsers(request):
	data = json.loads(request.body)
	id_lobby = data['id_lobby']
	try:
		lobby = Lobby.objects.get(id=id_lobby)
		AllUserInLobby = lobby.user.all()
		if len(AllUserInLobby) < 2:
			return JsonResponse({'status': 'ok', 'id_party': None})
		current_user = request.user
		user_found = find_compatibles_users(AllUserInLobby, current_user, lobby.id_game)
		if user_found:
			party = Party.objects.create(id_game=lobby.id_game, player1=current_user, player2=user_found, started_at=timezone.now())
			UserInLobby.objects.get(id_user=current_user, id_lobby=lobby).delete()
			UserInLobby.objects.get(id_user=user_found, id_lobby=lobby).delete()
			return JsonResponse({'status': 'ok', 'id_party': party.id})
			#send a notification to the user found ????????????????????
		else:
			return JsonResponse({'status': 'ok', 'id_party': None})
		#if id_party = NONE continue to wait
	except Lobby.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This lobby does not exist.'}, status=404)
	except UserInLobby.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'You are not in this lobby.'}, status=400)


# -------------------------------PUT LOBBY-----------------------------#
@login_required
@require_http_methods(['PUT'])
def ChangeLobbyName(request):
	data = json.loads(request.body)
	id_lobby = data['id_lobby']
	name = data['name']
	try:
		lobby = Lobby.objects.get(id=id_lobby)
		lobby.name = name
		lobby.save()
		return JsonResponse({'status': 'ok', 'message': 'The lobby name has been updated.'})
	except Lobby.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This lobby does not exist.'}, status=404)


# -------------------------------DELETE LOBBY-----------------------------#
@login_required
@require_http_methods(['DELETE'])
def deleteLobby(request):
	data = json.loads(request.body)
	id_lobby = data['id_lobby']
	try:
		lobby = Lobby.objects.get(id=id_lobby)
		lobby.delete()
		return JsonResponse({'status': 'ok', 'message': 'The lobby has been deleted.'})
	except Lobby.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This lobby does not exist.'}, status=404)
	
#useful especially for tournament