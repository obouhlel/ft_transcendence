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
		if 	data['firstname']:
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
		return JsonResponse({'status': 'error', 'message': 'Non authentifié.'}, status=401)

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

def list_games(request):
	if request.method == 'GET':
		if request.user.is_authenticated:
			games = list(Game.objects.values())
			data = []
			for game in games:
				data += [{
					'id': game.id,
					'name': game.name,
					'created_at': game.created_at.isoformat(),
				}]
			return JsonResponse({'status': 'ok', 'games': data})
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authenticated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'Invalid method.'}, status=405)

# add stats after a game to the user
# POST: ADD STATS
# PARAMS: score, game
# def add_stats(request):
# 	if request.method == 'POST':
# 		data = json.loads(request.body)
# 		if request.user.is_authenticated:
# 			if game == 'pong':
# 				request.user.pong_score = score
# 			elif game == 'shooter':
# 				request.user.shooter_score = score
# 			else:
# 				return JsonResponse({'status': 'error', 'message': 'Jeu inconnu.'}, status=400)
# 			request.user.save()
# 			return JsonResponse({'status': 'ok', 'message': 'Statistiques mises à jour avec succès.'})
# 		else:
# 			return JsonResponse({'status': 'error', 'message': 'Non authentifié.'}, status=401)
# 	else:
# 		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)
# friends
# GET: RETURN ALL FRIENDS
# POST: ADD FRIEND OR REMOVE FRIEND
# PARAMS: username, action
# FORMATS:
#
def friends(request):
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
			return JsonResponse({'status': 'error', 'message': 'Non authentifié.'}, status=401)
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
				return JsonResponse({'status': 'error', 'message': 'Cet utilisateur n\'existe pas.'}, status=404)
		elif action == 'decline':
			try:
				friend = CustomUser.objects.get(username=username)
				request.user.friend_requests.remove(friend)
				return JsonResponse({'status': 'ok', 'message': 'Demande d\'ami refusée avec succès.'})
			except CustomUser.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'Cet utilisateur n\'existe pas.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Action inconnue.'}, status=400)
	else:
		return JsonResponse({'status': 'error', 'message': 'Non authentifié.'}, status=401)

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
			return JsonResponse({'status': 'error', 'message': 'Non authentifié.'}, status=401)
	elif request.method == 'POST':
		if request.user.is_authenticated:
			try:
				friend = CustomUser.objects.get(username=username)
				request.user.friend_requests.add(friend)
				return JsonResponse({'status': 'ok', 'message': 'Demande d\'ami envoyée avec succès.'})
			except CustomUser.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'Cet utilisateur n\'existe pas.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Non authentifié.'}, status=401)
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
				return JsonResponse({'status': 'error', 'message': 'Cet utilisateur n\'existe pas.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Non authentifié.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)

#  get friend requests
# GET: RETURN ALL FRIEND REQUESTS
# PARAMS: username
def get_friend_requests(request):
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
			return JsonResponse({'status': 'error', 'message': 'Non authentifié.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)



