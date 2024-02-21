import json
import pytz
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from transcendence.models import CustomUser
from .models import Game, Party, Stat_Game, Lobby, Tournament, Stat_User_by_Game, friend_request, UserInLobby, PartyInTournament

def login_user(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		username = data['username']
		password = data['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			django_login(request, user)
			return JsonResponse({'status': 'ok', 'message': 'Vous êtes maintenant connecté en tant que ' + username})
		else:
			return JsonResponse({'status': 'error', 'message': 'Nom d\'utilisateur ou mot de passe incorrect.'}, status=401)

def register_user(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		username = data['username']
		password = data['password']
		password_confirm = data['password_confirm']
		email = data['email']
		firstname = data['firstname']
		lastname = data['lastname']
		sexe = data['sexe']
		birthdate = data['birthdate']

		# Valider que les données ne dépassent pas la longueur maximale autorisée
		data_list = [username, password, email, firstname, lastname]
		for data in data_list:
			if len(data) > 50:
				return JsonResponse({'status': 'error', 'message': 'Les données sont trop longues.'}, status=400)
		# verifier que le username n'est pas déjà utilisé
		if CustomUser.objects.filter(username=username).exists():
			return JsonResponse({'status': 'error', 'message': 'Ce username est déjà utilisé.'}, status=400)
		# Valider que l'email n'est pas déjà utilisé
		if CustomUser.objects.filter(email=email).exists():
			return JsonResponse({'status': 'error', 'message': 'Cet email est déjà utilisé.'}, status=400)
		# verifier que le mot de passe est la confirmation du mot de passe sont identiques
		if password != password_confirm:
			return JsonResponse({'status': 'error', 'message': 'Les mots de passe ne correspondent pas.'}, status=400)
		# Valider que le mot de passe contient au moins 8 caractères
		if len(password) < 8:
			return JsonResponse({'status': 'error', 'message': 'Le mot de passe doit contenir au moins 8 caractères.'}, status=400)
		# verifier que la date de naissance est valide
		try:
			birthdate = timezone.datetime.strptime(birthdate, '%Y-%m-%d').replace(tzinfo=pytz.UTC)
		except ValueError:
			return JsonResponse({'status': 'error', 'message': 'La date de naissance est invalide.'}, status=400)
		#verifier que la date de naissance n'est pas dans le futur
		if birthdate > timezone.now():
			return JsonResponse({'status': 'error', 'message': 'La date de naissance est dans le futur.'}, status=400)

		# Créer l'utilisateur
		user = CustomUser.objects.create(username=username, password=make_password(password), email=email, first_name=firstname, last_name=lastname ,sexe=sexe, birthdate=birthdate, date_joined=timezone.now())
		return JsonResponse({'status': 'ok', 'message': 'Votre compte a été créé avec succès.'})
	else:
		return JsonResponse({'status': 'error', 'message': 'Cette méthode n\'est pas autorisée.'}, status=405)

@csrf_exempt
def edit_profile(request):
	if request.method == 'POST':
		data = request.POST
		user = CustomUser.objects.get(username=request.user.username)
		if 	data['username']:
			username = data['username']
			if CustomUser.objects.filter(username=username).exists():
				return JsonResponse({'status': 'error', 'message': 'Ce username est déjà utilisé.'}, status=400)
			user.username = username
		if data['email']:
			email = data['email']
			if CustomUser.objects.filter(email=email).exists():
				return JsonResponse({'status': 'error', 'message': 'Cet email est déjà utilisé.'}, status=400)
			user.email = email
		if 	data['firstnammethodse']:
			user.first_name = data['firstname']
		if 	data['lastname']:
			user.last_name = data['lastname']
		if 	data['sexe']:
			user.sexe = data['sexe']
		if 	data['birthdate']:
			try:
				birthdate = timezone.datetime.strptime(data['birthdate'], '%Y-%m-%d').replace(tzinfo=pytz.UTC)
			except ValueError:
				return JsonResponse({'status': 'error', 'message': 'La date de naissance est invalide.'}, status=400)
			if birthdate > timezone.now():
				return JsonResponse({'status': 'error', 'message': 'La date de naissance est dans le futur.'}, status=400)
			user.birthdate = birthdate
		if 'avatar' in request.FILES and request.FILES['avatar']:
			user.avatar = request.FILES['avatar']
		if 	data['password'] and data['password_confirm']:
			password = data['password']
			password_confirm = data['password_confirm']
			if password != password_confirm:
				return JsonResponse({'status': 'error', 'message': 'Les mots de passe ne correspondent pas.'}, status=400)
			if len(password) < 8:
				return JsonResponse({'status': 'error', 'message': 'Le mot de passe doit contenir au moins 8 caractères.'}, status=400)
			user.password = make_password(password)
		user.save()
		return JsonResponse({'status': 'ok', 'message': 'Votre profil a été mis à jour avec succès !'})
	else:
		return JsonResponse({'status': 'error', 'message': 'Cette méthode n\'est pas autorisée.'}, status=405)

def logout_user(request):
	django_logout(request)
	return JsonResponse({'status': 'ok', 'message': 'Vous êtes maintenant déconnecté.'})

def profile(request):
	if request.user.is_authenticated:
		return JsonResponse({'status': 'ok', 'user': {
			'username': request.user.username,
			'email': request.user.email,
			'first_name': request.user.first_name,
			'last_name': request.user.last_name,
			'sexe': request.user.sexe,
			'birthdate': request.user.birthdate.isoformat(),
			'avatar': request.user.avatar.url if request.user.avatar else None,
		}})
	else:
		return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
############################################################################
	
# def require_GET(func):
# 	def wrapper(request, *args, **kwargs):
# 		if request.method == 'GET':
# 			return func(request, *args, **kwargs)
# 		else:
# 			return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)
# 	return wrapper

# def require_POST(func):
# 	def wrapper(request, *args, **kwargs):
# 		if request.method == 'POST':
# 			return func(request, *args, **kwargs)
# 		else:
# 			return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)
# 	return wrapper

#@require_http_methods(['GET'])
#@require_authenticated


def stat_game_data(stat_game):
	data = {
		'nb_played': stat_game.nb_played,
		'time_played': stat_game.time_played,
		'nb_party': stat_game.nb_party,
	}
	return data

def stat_user_by_game_data(stat_user):
	data = {
		'nb_played': stat_user.nb_played,
		'time_played': stat_user.time_played,
		'nb_win': stat_user.nb_win,
		'nb_lose': stat_user.nb_lose,
	}
	return data

def user_data(user):
	data = {
		'username': user.username,
		'email': user.email,
		'first_name': user.first_name,
		'last_name': user.last_name,
		'sexe': user.sexe,
		'birthdate': user.birthdate.isoformat(),
		'avatar': user.avatar.url if user.avatar else None,
		'is_authenticated': user.is_authenticated,
		'stat': stat_user_by_game_data(user.stat),
		'friends': [friend.username for friend in user.friends.all()],
		'blocked': [blocked.username for blocked in user.list_blocked.all()],
		'friend_request': [friend_request.id for friend_request in user.friend_request.all()]
	}
	return data

def game_data(game):
	data = {
		'id': game.id,
		'name': game.name,
		'description': game.description,
		'genre': game.genre,
		'image': game.image,
		'created_at': game.created_at.isoformat(),
		'point_to_win': game.point_to_win,
		'stat': stat_game_data(game.stat),
		'lobby': [lobby_data(lobby) for lobby in game.lobby_game.all()],
		'party': [party_data(party) for party in game.party_game.all()],
		'tournament': [tournament_data(tournament) for tournament in game.tournament_game.all()]
	}
	return data

def UserInLobby_data(userInLobby):
	data = {
		'id': userInLobby.id,
		'id_user': user_data(userInLobby.id_user),
		'id_lobby': lobby_data(userInLobby.id_lobby),
		'entry_at': userInLobby.entry_at.isoformat(),
	}
	return data

def lobby_data(lobby):
	data = {
		'id': lobby.id,
		'type': lobby.type,
		'id_game': lobby.id_game,
		'user': [UserInLobby_data(userInLobby) for userInLobby in lobby.user.all()]
	}
	return data

def party_data(party):
	data = {
		'id': party.id,
		'id_game': party.id_game,
		'player1': user_data(party.player1),
		'player2': user_data(party.player2),
		'score1': party.score1,
		'score2': party.score2,
		'id_winner': party.id_winner,
		'id_loser': party.id_loser,
		'started_at': party.started_at.isoformat(),
		'ended_at': party.ended_at.isoformat(),
		'time_played': party.time_played,
		'type': party.type,
	}
	return data

def tournament_data(tournament):
	data = {
		'id': tournament.id,
		'type': tournament.type,
		'id_game': tournament.id_game,
		'lobby': lobby_data(tournament.lobby_tournament),
		'party': [party_data(party) for party in tournament.party_tournament.all()]
	}
	return data


def friend_request_data(friend_request):
	data = {
		'id': friend_request.id,
		'id_sender': user_data(friend_request.id_sender),
		'id_receiver': user_data(friend_request.id_receiver),
		'created_at': friend_request.created_at.isoformat(),
		'status': friend_request.status,
	}
	return data

def user_in_lobby_data(user_in_lobby):
	data = {
		'id': user_in_lobby.id,
		'id_user': user_data(user_in_lobby.id_user),
		'id_lobby': lobby_data(user_in_lobby.id_lobby),
	}
	return data

def party_in_tournament_data(party_in_tournament):
	data = {
		'id': party_in_tournament.id,
		'match': party_data(party_in_tournament.match),
		'round_nb': party_in_tournament.round_nb,
		'id_tournament': tournament_data(party_in_tournament.id_tournament),
	}
	return data

#---------------------------------GET---------------------------------#
# -------------------------------GET USER-----------------------------#
@login_required
@require_http_methods(['GET'])
def getUserName(request):
	return JsonResponse({'username': request.user.username})

@login_required
@require_http_methods(['GET'])
def getUserByName(request, username):
	try:
		user = CustomUser.objects.get(username=username)
		data = user_data(user)
		return JsonResponse({'status': 'ok', 'user': data})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)

@login_required
@require_http_methods(['GET'])
def getUserById(request, id):
	try:
		user = CustomUser.objects.get(id=id)
		data = user_data(user)
		return JsonResponse({'status': 'ok', 'user': data})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)

@login_required
@require_http_methods(['GET'])
def getAllUsers(request):
	users = CustomUser.objects.all()
	data = []
	for user in users:
		data += [user_data(user)]
	return JsonResponse({'status': 'ok', 'users': data})

# -------------------------------GET GAME-----------------------------#
@login_required
@require_http_methods(['GET'])
def getGameByName(request, name):
	try:
		game = Game.objects.get(name=name)
		data = game_data(game)
		return JsonResponse({'status': 'ok', 'game': data})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
	
@login_required
@require_http_methods(['GET'])
def getGameById(request, id):
	try:
		game = Game.objects.get(id=id)
		data = game_data(game)
		return JsonResponse({'status': 'ok', 'game': data})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
	
@login_required
@require_http_methods(['GET'])
def getAllGames(request):
	games = Game.objects.all()
	data = []
	for game in games:
		data += [game_data(game)]
	return JsonResponse({'status': 'ok', 'games': data})

#---------------------------------GET LOBBY---------------------------------#

@login_required
@require_http_methods(['GET'])
def getLobbyById(request, id):
	try:
		lobby = Lobby.objects.get(id=id)
		data = lobby_data(lobby)
		return JsonResponse({'status': 'ok', 'lobby': data})
	except Lobby.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This lobby does not exist.'}, status=404)
	
@login_required
@require_http_methods(['GET'])
def getAllLobbies(request):
	lobbies = Lobby.objects.all()
	data = []
	for lobby in lobbies:
		data += [lobby_data(lobby)]
	return JsonResponse({'status': 'ok', 'lobbies': data})

@login_required
@require_http_methods(['GET'])
def getLobbyByGame(request, id_game):
	try:
		game = Game.objects.get(id=id_game)
		lobbies = game.lobby_game.all()
		data = [lobby_data(lobby) for lobby in lobbies]
		return JsonResponse({'status': 'ok', 'lobbies': data})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
	
@login_required
@require_http_methods(['GET'])
def getUserInLobby(request, id_lobby):
	try:
		lobby = Lobby.objects.get(id=id_lobby)
		users = lobby.user.all()
		data = [UserInLobby_data(userInLobby) for userInLobby in users]
		return JsonResponse({'status': 'ok', 'lobby': data})
	except Lobby.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This lobby does not exist.'}, status=404)

#---------------------------------GET PARTY---------------------------------#
@login_required
@require_http_methods(['GET'])
def getPartyById(request, id):
	try:
		party = Party.objects.get(id=id)
		data = party_data(party)
		return JsonResponse({'status': 'ok', 'party': data})
	except Party.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This party does not exist.'}, status=404)

@login_required
@require_http_methods(['GET'])
def getAllParties(request):
	parties = Party.objects.all()
	data = []
	for party in parties:
		data += [party_data(party)]
	return JsonResponse({'status': 'ok', 'parties': data})

@login_required
@require_http_methods(['GET'])
def getPartyByGame(request, id_game):
	try:
		game = Game.objects.get(id=id_game)
		parties = game.party_game.all()
		data = [party_data(party) for party in parties]
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
		data = [user_data(user) for user in users]
		return JsonResponse({'status': 'ok', 'party': data})
	except Party.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This party does not exist.'}, status=404)
#---------------------------------GET TOURNAMENT---------------------------------#
@login_required
@require_http_methods(['GET'])
def getTournamentById(request, id):
	try:
		tournament = Tournament.objects.get(id=id)
		data = tournament_data(tournament)
		return JsonResponse({'status': 'ok', 'tournament': data})
	except Tournament.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This tournament does not exist.'}, status=404)
	
@login_required
@require_http_methods(['GET'])
def getAllTournaments(request):
	tournaments = Tournament.objects.all()
	data = []
	for tournament in tournaments:
		data += [tournament_data(tournament)]
	return JsonResponse({'status': 'ok', 'tournaments': data})

@login_required
@require_http_methods(['GET'])
def getTournamentByGame(request, id_game):
	try:
		game = Game.objects.get(id=id_game)
		tournaments = game.tournament_game.all()
		data = [tournament_data(tournament) for tournament in tournaments]
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
		data = lobby_data(lobby)
		return JsonResponse({'status': 'ok', 'lobby': data})
	except Tournament.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This tournament does not exist.'}, status=404)
#---------------------------------GET STAT---------------------------------#
@login_required
@require_http_methods(['GET'])
def getStatByUser(request, id_user):
	try:
		user = CustomUser.objects.get(id=id_user)
		data = stat_user_by_game_data(user.stat)
		return JsonResponse({'status': 'ok', 'stat': data})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)
	
@login_required
@require_http_methods(['GET'])
def getStatByGame(request, id_game):
	try:
		game = Game.objects.get(id=id_game)
		data = stat_game_data(game.stat)
		return JsonResponse({'status': 'ok', 'stat': data})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)

#---------------------------------GET FRIEND---------------------------------#
@login_required
@require_http_methods(['GET'])
def getAllFriendsofUser(request, id_user):
	try:
		user = CustomUser.objects.get(id=id_user)
		data = [user_data(friend) for friend in user.friends.all()]
		return JsonResponse({'status': 'ok', 'friends': data})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)
	
@login_required
@require_http_methods(['GET'])
def getAllFriendRequestofUser(request, id_user):
	try:
		user = CustomUser.objects.get(id=id_user)
		data = [friend_request_data(friend_request) for friend_request in user.friend_request.all()]
		return JsonResponse({'status': 'ok', 'friend_request': data})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)
	


#---------------------------------POST---------------------------------#
# -------------------------------POST LOBBY-----------------------------#
	
def newLobby(id_game, type, name):
	lobby = Lobby.objects.create(id_game=id_game, type=type, name=name)
	return lobby

#when User click on Play button of a game, 
#it will create a lobby if there is no lobby for this game
# method POST
#in request body: id_game
#return: id_lobby
#create a UserInLobby for the user with entry_at = now
@login_required
@require_http_methods(['POST'])
def joinLobby(request):
	data = json.loads(request.body)
	id_game = data['id_game']
	try:
		game = Game.objects.get(id=id_game)
		lobby = game.lobby_game.all()
		if len(lobby) == 0:
			lobby = newLobby(game, 'Public', 'Lobby')
		else:
			lobby = lobby[0]
		user = request.user
		userInLobby = UserInLobby.objects.create(id_user=user, id_lobby=lobby)
		Lobby.objects.get(id=lobby.id).user.add(userInLobby)
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
		userInLobby = UserInLobby.objects.get(id_user=request.user, id_lobby=lobby)
		Lobby.objects.get(id=lobby.id).user.remove(userInLobby)
		userInLobby.delete()
		return JsonResponse({'status': 'ok', 'message': 'You have left the lobby.'})
	except Lobby.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This lobby does not exist.'}, status=404)
	except UserInLobby.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'You are not in this lobby.'}, status=400)


def find_user_with_most_compatible_ratio(users, current_user):
	if len(users) == 0:
		return None
	compatible = None
	current_user_stat = current_user.stat
	ratio = 0
	for user in users:
		if user != current_user:
			user_stat = user.stat
			if compatible == None:
				compatible = user
			else:
				ratio = abs(user_stat.nb_win/user_stat.nb_played - current_user_stat.nb_win/current_user_stat.nb_played)

	

def find_compatibles_users(users, current_user):
	compatible = None
	now = timezone.now()
	waiting_time = now - current_user.entry_at
	#example: if the player wait for 1 second, the tolerance is 10%
	#if the player wait for 2 seconds, the tolerance is 20%
	#if the player wait for 3 seconds, the tolerance is 30%

	toleance =  waiting_time.seconds / 10

	#find the most compatible users with the acceptable tolerance
	current_user_stat = current_user.stat
	for user in users:
		if user != current_user:
			user_stat = user.stat
			if abs(user_stat.nb_win/user_stat.nb_played - current_user_stat.nb_win/current_user_stat.nb_played) <= toleance:
				compatible = user
				break
		else:
			pass
	#how to prevent the user to wait for too long
	if compatible == None and waiting_time.seconds > 30:
		compatible = find_user_with_most_compatible_ratio(users, current_user)
		if compatible == None:
			return None
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
	#find the most compatible users with the acceptable tolerance
	#the more the player wait, the toleance increases
	#example: if the player wait for 2 seconds, the tolerance is 10%
	#if the player wait for 30 seconds, the tolerance is 100%
	#the tolerance is the difference between the ratio of win/played of the users

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
	except Lobby.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This lobby does not exist.'}, status=404)
	except UserInLobby.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'You are not in this lobby.'}, status=400)

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
	

@login_required
@require_http_methods(['POST'])
def addPointToParty(request, id_party):
	try:
		party = Party.objects.get(id=id_party)
		if party.player1 == request.user:
			party.score1 += 1
		elif party.player2 == request.user:
			party.score2 += 1
		else:
			return JsonResponse({'status': 'error', 'message': 'This user is not in this party.'}, status=400)
		party.save()
		if (party.score1 == party.id_game.point_to_win or party.score2 == party.id_game.point_to_win):
			return (endParty(request, id_party))
		return JsonResponse({'status': 'ok', 'message': 'Point added successfully.'})
	except Party.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This party does not exist.'}, status=404)



# MATCHMAKER: FIND THE MOST COMPATIBLE USERS WITH THE SAME RATIO OF WIN/PLAYED
# THE MORE THE PLAYER WAIT, THE TOLEANCE INCREASES
# EXAMPLE: IF THE PLAYER WAIT FOR 10 SECONDS, THE TOLERANCE IS 10%
# IF THE PLAYER WAIT FOR 1 MINUTE, THE TOLERANCE IS 100%
#THE TOLERENCE IS THE DIFFERENCE BETWEEN THE RATIO OF WIN/PLAYED OF THE USERS
#MAXIMUM TOLERANCE IS 100%
	

def find_compatibles_users(users, current_user, game):
	compatible = None
	

	return compatible

@login_required
@require_http_methods(['POST'])
def FindMatch(request, id_game, id_lobby):
	try:
		game = Game.objects.get(id=id_game)
		lobby = Lobby.objects.get(id=id_lobby)
		users = lobby.user.all()
		current_user = request.user
		found = find_compatibles_users(users, current_user, game)










def home(request):
	html = render_to_string('home.html', request=request)
	return HttpResponse(html)

def games(request):
	if request.user.is_authenticated:
		data = {
			'message': 'Bienvenue sur la page des jeux!',
			'status': 'ok'
		}
		return JsonResponse(data)

def game(request):
	data = {
		'message': 'Bienvenue sur la page du jeu!',
	}
	return JsonResponse(data)


def pong(request):
	return getUserName(request)

def shooter(request):
	return getUserName(request)



# add stats after a game to the user
# POST: ADD STATS
# PARAMS: score, game
def add_stats_users_by_game(request, id_party):
	if request.method == 'POST':
		if request.user.is_authenticated:
			try:
				party = Party.objects.get(id=id_party)
				stat_user = request.user.stat.get(game=party.id_game)
				stat_user.nb_played += 1
				stat_user.time_played += (party.ended_at - party.started_at).seconds
				if party.id_winner == request.user:
					stat_user.nb_win += 1
				else:
					stat_user.nb_lose += 1
				stat_user.save()
				return JsonResponse({'status': 'ok', 'message': 'Statistiques mises à jour avec succès.'})
			except Party.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This party doesn\'t exist.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)


# add stats after a game to the game
# POST: ADD STATS
# PARAMS: score, game
def add_stats_game(request, id_party):
	if request.method == 'POST':
		if request.user.is_authenticated:
			try:
				party = Party.objects.get(id=id_party)
				stat_game = party.id_game.stat
				stat_game.nb_played += 1
				stat_game.time_played += paty
				stat_game.nb_party += 1
				stat_game.save()
				return JsonResponse({'status': 'ok', 'message': 'Statistiques mises à jour avec succès.'})
			except Party.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This party doesn\'t exist.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)

# friends
# GET: RETURN ALL FRIENDS
# POST: ADD FRIEND OR REMOVE FRIEND
# PARAMS: username, action
# FORMATS:
#
def get_all_friends(request):
	if request.method == 'GET':
		if request.user.is_authenticated:
			friends = request.user.friends.all()
			data = []
			for friend in friends:
				data += [{
					'username': friend.username,
					'email': friend.email,
					'first_name': friend.first_name,
					'last_name': friend.last_name,
					'sexe': friend.sexe,
					'birthdate': friend.birthdate.isoformat(),
					'avatar': friend.avatar.url if friend.avatar else None,
					'is_authenticated': friend.is_authenticated,
				}]
			return JsonResponse({'status': 'ok', 'friends': data})
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)


#get_all_request
# GET: RETURN ALL FRIEND REQUESTS
# PARAMS: user
def get_all_request(request):
	if request.method == 'GET':
		if request.user.is_authenticated:
			requests = request.user.list_request.all()
			data = []
			for user in requests:
				data += [{
					'username': user.username,
					'email': user.email,
					'first_name': user.first_name,
					'last_name': user.last_name,
					'sexe': user.sexe,
					'birthdate': user.birthdate.isoformat(),
					'avatar': user.avatar.url if user.avatar else None,
					'is_authenticated': user.is_authenticated,
				}]
			return JsonResponse({'status': 'ok', 'requests': data})
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)


# friend_requests
# POST: ACCEPT FRIEND REQUEST OR DECLINE FRIEND REQUEST
# PARAMS: username, action
# FORMATS:
#
def respond_to_friend_request(request):
	data = json.loads(request.body)
	username = data['username']
	action = data['action']
	if request.user.is_authenticated:
		if action == 'accept':
			try:
				friend = CustomUser.objects.get(username=username)
				request.user.friend_requests.remove(friend)
				request.user.friends.add(friend)
				return JsonResponse({'status': 'ok', 'message': 'Demande d\'ami acceptée avec succès.'})
			except CustomUser.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)
		elif action == 'decline':
			try:
				friend = CustomUser.objects.get(username=username)
				request.user.friend_requests.remove(friend)
				return JsonResponse({'status': 'ok', 'message': 'Demande d\'ami refusée avec succès.'})
			except CustomUser.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Action inconnue.'}, status=400)
	else:
		return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)

# friend_requests
# GET: RETURN ALL FRIEND REQUESTS
# POST: SEND FRIEND REQUEST
# PARAMS: username, action
# FORMATS:
def request_friend(request):
	data = json.loads(request.body)
	username = data['username']
	action = data['action']
	if request.method == 'GET':
		if request.user.is_authenticated:
			friend_requests = request.user.friend_requests.all()
			data = []
			for friend in friend_requests:
				data += [{
					'username': friend.username,
					'avatar': friend.avatar.url if friend.avatar else None,
				}]
			return JsonResponse({'status': 'ok', 'friend_requests': data})
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	elif request.method == 'POST':
		if request.user.is_authenticated:
			try:
				friend = CustomUser.objects.get(username=username)
				request.user.friend_requests.add(friend)
				return JsonResponse({'status': 'ok', 'message': 'Demande d\'ami envoyée avec succès.'})
			except CustomUser.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)

#remove friend
# POST: REMOVE FRIEND
# PARAMS: username
def remove_friend(request):
	data = json.loads(request.body)
	username = data['username']
	if request.method == 'POST':
		if request.user.is_authenticated:
			try:
				friend = CustomUser.objects.get(username=username)
				request.user.friends.remove(friend)
				return JsonResponse({'status': 'ok', 'message': 'Ami retiré avec succès.'})
			except CustomUser.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)




# put user in tournament
# POST: PUT USER IN TOURNAMENT
# PARAMS: id_game, id_tournament
# 

#make a party in a tournament
# POST: MAKE A PARTY IN TOURNAMENT
# PARAMS: id_game, id_tournament
#Generate matches for a list of players

# powers of two always have exactly one bit set to 1. When you subtract 1 from a power of two, 
# all the bits to the right of the set bit become 1. 
# Therefore, performing a bitwise AND operation with the original number and 
# the number minus one will always result in zero for powers of two 5.
def is_power_of_two(n):
	return n > 0 and (n & (n - 1)) == 0
