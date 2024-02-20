import json
import pytz
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from transcendence.models import CustomUser
from django.conf import settings
from django.shortcuts import redirect
import requests
from .models import Game, Party, Stat_Game, Lobby

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

def login_42(request):
	if request.method == 'GET':
		code = request.GET.get('code')
		if code:
			token_url = 'https://api.intra.42.fr/oauth/token'

			client_id = settings.API_42_UID
			secret_key = settings.API_42_SECRET
			redirect_uri = settings.API_42_REDIRECT_URI

			data = {
				'grant_type': 'authorization_code',
				'client_id': client_id,
				'client_secret': secret_key,
				'code': code,
				'redirect_uri': redirect_uri,
			}
			response = requests.post(token_url, data=data)
			if response.status_code == 200:
				access_token = response.json()['access_token']
				token_type = response.json()['token_type']
				user_url = 'https://api.intra.42.fr/v2/me'
				headers = {
					'Authorization': token_type + ' ' + access_token,
				}
				response = requests.get(user_url, headers=headers)
				if response.status_code == 200:
					user_data = response.json()
					username = user_data['login']
					email = user_data['email']
					firstname = user_data['first_name']
					lastname = user_data['last_name']
					if CustomUser.objects.filter(token=access_token).exists():
						user = CustomUser.objects.get(username=username)
						django_login(request, user)
						return redirect('/')
					else:
						if CustomUser.objects.filter(username=username).exists():
							return JsonResponse({'status': 'error', 'message': 'Ce username est déjà utilisé.'}, status=400)
						user = CustomUser.objects.create(username=username, email=email, first_name=firstname, last_name=lastname, token=access_token, date_joined=timezone.now())
						django_login(request, user)
						return redirect('/')
				else:
					return JsonResponse({'status': 'error', 'message': 'Impossible de récupérer les données de l\'utilisateur.'}, status=400)
			else:
				return JsonResponse({'status': 'error', 'message': 'Impossible de récupérer le token d\'accès.'}, status=400)
		else:
			return JsonResponse({'status': 'error', 'message': 'Code invalide.'}, status=400)
	else:
		return JsonResponse({'status': 'error', 'message': 'Cette méthode n\'est pas autorisée.'}, status=405)

def register_user(request):
	if request.method == 'POST':
		data = request.POST
		username = data.get('username')
		password = data.get('password')
		password_confirm = data.get('password_confirm')
		email = data.get('email')
		firstname = data.get('firstname')
		lastname = data.get('lastname')
		sexe = data.get('sexe')
		birthdate = data.get('birthdate')

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
		if 'avatar' in request.FILES:
			user.avatar = request.FILES['avatar']
		else :
			user.avatar = 'no_avatar.png'
		user.save()
		return JsonResponse({'status': 'ok', 'message': 'Votre compte a été créé avec succès.'})
	else:
		return JsonResponse({'status': 'error', 'message': 'Cette méthode n\'est pas autorisée.'}, status=405)

def edit_profile(request):
	if request.method == 'POST':
		data = request.POST
		try:
			user = CustomUser.objects.get(username=request.user.username)
		except CustomUser.DoesNotExist:
			return JsonResponse({'status': 'error', 'message': 'Utilisateur non trouvé.'}, status=404)

		username = data.get('username')
		if username and username != user.username:
			if CustomUser.objects.filter(username=username).exists():
				return JsonResponse({'status': 'error', 'message': 'Ce username est déjà utilisé.'}, status=400)
			user.username = username

		email = data.get('email')
		if email and email != user.email:
			if CustomUser.objects.filter(email=email).exists():
				return JsonResponse({'status': 'error', 'message': 'Cet email est déjà utilisé.'}, status=400)
			user.email = email

		first_name = data.get('firstname', user.first_name)
		if first_name:
			user.first_name = first_name
		last_name = data.get('lastname', user.last_name)
		if last_name:
			user.last_name = last_name
		sexe = data.get('sexe', user.sexe)
		if sexe:
			user.sexe = data.get('sexe', user.sexe)

		birthdate = data.get('birthdate')
		if birthdate:
			try:
				birthdate = timezone.datetime.strptime(birthdate, '%Y-%m-%d').replace(tzinfo=pytz.UTC)
				if birthdate > timezone.now():
					return JsonResponse({'status': 'error', 'message': 'La date de naissance est dans le futur.'}, status=400)
				user.birthdate = birthdate
			except ValueError:
				return JsonResponse({'status': 'error', 'message': 'La date de naissance est invalide.'}, status=400)

		if 'avatar' in request.FILES:
			user.avatar = request.FILES['avatar']

		password = data.get('password')
		password_confirm = data.get('password_confirm')
		if password and password_confirm:
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

def getUserName(request):
	if request.user.is_authenticated:
		data = {
			'username': request.user.username,
			'email': request.user.email,
			'first_name': request.user.first_name,
			'last_name': request.user.last_name,
			'sexe': request.user.sexe,
			'birthdate': request.user.birthdate.isoformat(),
			'is_staff': request.user.is_staff,
			'is_superuser': request.user.is_superuser,
			'csrf_token': request.META['CSRF_COOKIE'],
		}
		return JsonResponse(data)
	else:
		return JsonResponse({'status': 'error', 'message': 'Not authenticated'}, status=401)

def pong(request):
	return getUserName(request)

def shooter(request):
	return getUserName(request)

def get_all_games(request):
	if request.method == 'GET':
		if request.user.is_authenticated:
			games = Game.objects.all()
			data = []
			for game in games:
				data += [{
					'id': game.id,
					'name': game.name,
					'description': game.description,
					'genre': game.genre,
					'image': game.image,
					'created_at': game.created_at.isoformat(),
					'stat': {
						'nb_played': game.stat.nb_played,
						'time_played': game.stat.time_played,
						'nb_party': game.stat.nb_party,
					}
				}]
			return JsonResponse({'status': 'ok', 'games': data})
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authenticated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'Invalid method.'}, status=405)

# get game by name
def get_game_by_name(request, name):
	if request.method == 'GET':
		if request.user.is_authenticated:
			try:
				game = Game.objects.get(name=name)
				data = {
					'id': game.id,
					'name': game.name,
					'description': game.description,
					'genre': game.genre,
					'image': game.image,
					'created_at': game.created_at.isoformat(),
					'stat': {
						'nb_played': game.stat.nb_played,
						'time_played': game.stat.time_played,
						'nb_party': game.stat.nb_party,
					}
				}
				return JsonResponse({'status': 'ok', 'game': data})
			except Game.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authenticated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'Invalid method.'}, status=405)

# get game by id
def get_game_by_id(request, id):
	if request.method == 'GET':
		if request.user.is_authenticated:
			try:
				game = Game.objects.get(id=id)
				data = {
					'id': game.id,
					'name': game.name,
					'description': game.description,
					'genre': game.genre,
					'image': game.image,
					'created_at': game.created_at.isoformat(),
					'stat': {
						'nb_played': game.stat.nb_played,
						'time_played': game.stat.time_played,
						'nb_party': game.stat.nb_party,
					}
				}
				return JsonResponse({'status': 'ok', 'game': data})
			except Game.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authenticated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'Invalid method.'}, status=405)


# get all users
def get_all_users(request):
	if request.method == 'GET':
		if request.user.is_authenticated:
			users = CustomUser.objects.all()
			data = []
			for user in users:
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
			return JsonResponse({'status': 'ok', 'users': data})
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)

# get user by username
def get_user_by_username(request, username):
	if request.method == 'GET':
		if request.user.is_authenticated:
			try:
				user = CustomUser.objects.get(username=username)
				data = {
					'username': user.username,
					'email': user.email,
					'first_name': user.first_name,
					'last_name': user.last_name,
					'sexe': user.sexe,
					'birthdate': user.birthdate.isoformat(),
					'avatar': user.avatar.url if user.avatar else None,
					'is_authenticated': user.is_authenticated,
				}
				return JsonResponse({'status': 'ok', 'user': data})
			except CustomUser.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)
# get user by id
def get_user_by_id(request, id):
	if request.method == 'GET':
		if request.user.is_authenticated:
			try:
				user = CustomUser.objects.get(id=id)
				data = {
					'username': user.username,
					'email': user.email,
					'first_name': user.first_name,
					'last_name': user.last_name,
					'sexe': user.sexe,
					'birthdate': user.birthdate.isoformat(),
					'avatar': user.avatar.url if user.avatar else None,
					'is_authenticated': user.is_authenticated,
				}
				return JsonResponse({'status': 'ok', 'user': data})
			except CustomUser.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)
			else:
				return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)

# get lobby users
def get_all_user_in_all_lobby(request, id_game):
	if request.method == 'GET':
		if request.user.is_authenticated:
			try:
				game = Game.objects.get(id=id_game)
				lobbies = game.lobby_game.all()
				# get all users in the lobby
				data = []
				for lobby in lobbies:
					users = lobby.user.all()
					for user in users:
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
				return JsonResponse({'status': 'ok', 'lobby': data})
			except Game.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This game doesn\'t exist.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)


#get user in a lobby of a game
def get_user_in_lobby(request, id_game, id_lobby):
	if request.method == 'GET':
		if request.user.is_authenticated:
			try:
				game = Game.objects.get(id=id_game)
				lobby = game.lobby_game.get(id=id_lobby)
				users = lobby.user.all()
				data = []
				for user in users:
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
				return JsonResponse({'status': 'ok', 'lobby': data})
			except Lobby.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This lobby doesn\'t exist.'}, status=404)
			except Game.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This game doesn\'t exist.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)


#get_user_in_party
def get_user_in_party(request, id_party):
	if request.method == 'GET':
		if request.user.is_authenticated:
			try:
				party = Party.objects.get(id=id_party)
				data = {
					'id': party.id,
					'id_game': party.id_game,
					'name': party.name,
					'started_at': party.started_at.isoformat(),
					'ended_at': party.ended_at.isoformat(),
					'score1': party.score1,
					'score2': party.score2,
					'id_winner': party.id_winner,
					'id_loser': party.id_loser,
				}
				return JsonResponse({'status': 'ok', 'party': data})
			except Party.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This party doesn\'t exist.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)


#put user in lobby
def put_user_in_lobby(request, id_game, id_lobby):
	if request.method == 'POST':
		if request.user.is_authenticated:
			try:
				game = Game.objects.get(id=id_game)
				lobby = game.lobby_game.get(id=id_lobby)
				lobby.user.add(request.user)
				return JsonResponse({'status': 'ok', 'message': 'Utilisateur ajouté avec succès.'})
			except Lobby.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This lobby doesn\'t exist.'}, status=404)
			except Game.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This game doesn\'t exist.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)

#remove user from lobby
def remove_user_from_lobby(request, id_game):
	if request.method == 'POST':
		if request.user.is_authenticated:
			try:
				game = Game.objects.get(id=id_game)
				game.lobby.remove(request.user)
				return JsonResponse({'status': 'ok', 'message': 'Utilisateur retiré avec succès.'})
			except Game.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This game doesn\'t exist.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)

# put user in party : pick 2 users that are in the lobby and put them in a party
# take the most compatible users with the same ratio of win/played
def put_user_in_party(request, id_game):
	if request.method == 'POST':
		if request.user.is_authenticated:
			try:
				game = Game.objects.get(id=id_game)
				lobby = game.lobby.all()
				if len(lobby) < 2:
					return JsonResponse({'status': 'error', 'message': 'Pas assez de joueurs dans le lobby.'}, status=400)
				else:
					# get the most compatible users
					most_compatible = None
					for user1 in lobby:
						for user2 in lobby:
							if user1 != user2:
								stat_user1 = user1.stat.get(game=game)
								stat_user2 = user2.stat.get(game=game)
								ratio1 = stat_user1.nb_win / stat_user1.nb_played if stat_user1.nb_played > 0 else 0
								ratio2 = stat_user2.nb_win / stat_user2.nb_played if stat_user2.nb_played > 0 else 0
								if most_compatible is None or abs(ratio1 - ratio2) < most_compatible[0]:
									most_compatible = (abs(ratio1 - ratio2), user1, user2)
					# create the party
					party = Party.objects.create(id_game=game, player1=most_compatible[1], player2=most_compatible[2],\
					 started_at=timezone.now())
					# remove the users from the lobby
					game.lobby.remove(most_compatible[1])
					game.lobby.remove(most_compatible[2])
					return JsonResponse({'status': 'ok', 'message': 'Partie créée avec succès.'})
			except Game.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This game doesn\'t exist.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)


#add points to the user in the party
def add_point(request, id_party):
	if request.method == 'POST':
		if request.user.is_authenticated:
			try:
				party = Party.objects.get(id=id_party)
				if party.player1 == request.user:
					party.score1 += 1
				elif party.player2 == request.user:
					party.score2 += 1
				else:
					return JsonResponse({'status': 'error', 'message': 'This user is not in this party.'}, status=400)
				if (party.score1 == party.id_game.point_to_win or party.score2 == party.id_game.point_to_win):
					return (end_party(request, id_party))
				return JsonResponse({'status': 'ok', 'message': 'Point ajouté avec succès.'})
			except Party.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This party doesn\'t exist.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)


#end party
def end_party(request, id_party):
	if request.method == 'POST':
		if request.user.is_authenticated:
			try:
				party = Party.objects.get(id=id_party)
				if party.score1 > party.score2:
					party.id_winner = party.player1
					party.id_loser = party.player2
				else:
					party.id_winner = party.player2
					party.id_loser = party.player1
				party.ended_at = timezone.now()
				party.time_played = (party.ended_at - party.started_at).seconds
				party.save()
				return JsonResponse({'status': 'ok', 'message': 'Partie terminée avec succès.'})
			except Party.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This party doesn\'t exist.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)


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

# get_all_blocked
# GET: RETURN ALL BLOCKED USERS
# PARAMS: username
def get_all_blocked(request):
	if request.method == 'GET':
		if request.user.is_authenticated:
			blocked = request.user.list_blocked.all()
			data = []
			for user in blocked:
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
			return JsonResponse({'status': 'ok', 'blocked': data})
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
