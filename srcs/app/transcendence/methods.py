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
		data = json.loads(request.body)
		user = CustomUser.objects.get(username=request.user.username)
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
	data = {
		'message': 'Bienvenue sur la page des jeux!',
	}
	return JsonResponse(data)

def game(request):
	data = {
		'message': 'Bienvenue sur la page du jeu!',
	}
	return JsonResponse(data)

def pong(request):
	data = {
		'message': 'Bienvenue sur la page du jeu Pong!',
	}
	return JsonResponse(data)

def shooter(request):
	data = {
		'message': 'Bienvenue sur la page du jeu Shooter!',
	}
	return JsonResponse(data)
