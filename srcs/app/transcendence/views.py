# views.py
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from transcendence.models import CustomUser
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
import json
import pytz

def index(request):
	return render(request, 'index.html')

def section(request, section):
	if section == 'home':
		return HttpResponse(render_to_string('views/home.html', request=request))
	elif section == 'login':
		return HttpResponse(render_to_string('views/login.html', request=request))
	elif section == 'register':
		return HttpResponse(render_to_string('views/register.html', request=request))
	elif section == 'profile':
		return HttpResponse(render_to_string('views/profile.html', request=request))
	elif section == 'games':
		return HttpResponse(render_to_string('views/games.html', request=request))
	elif section == 'game':
		return HttpResponse(render_to_string('views/game.html', request=request))
	elif section == 'pong':
		return HttpResponse(render_to_string('views/pong.html', request=request))
	elif section == 'shooter':
		return HttpResponse(render_to_string('views/shooter.html', request=request))
	else:
		return JsonResponse({'status': 'error', 'message': 'Section inconnue.'}, status=404)

@csrf_exempt
def login_user(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		username = data['username']
		password = data['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			django_login(request, user)
			return JsonResponse({'status': 'ok', 'message': 'Vous êtes maintenant connecté en tant que ' + username})

@csrf_exempt
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

		# Vos validations ici...

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

		# Vos validations et mises à jour ici...

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
	html = render_to_string('views/home.html', request=request)
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
