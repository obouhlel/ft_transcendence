from django.shortcuts import render, redirect
from transcendence.models import CustomUser # mon propre model
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout #test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #test
from django.views.decorators.csrf import csrf_exempt
import pytz
import json

def index(request):
	return render(request, 'index.html')

def logout_user(request):
	django_logout(request)
	messages.success(request, 'Vous êtes maintenant déconnecté.')
	return JsonResponse({'status': 'ok', 'message': 'Vous êtes maintenant déconnecté.'})

# Create your views here.
# @csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            messages.success(request, 'Vous êtes maintenant connecté.')
            return JsonResponse({'status': 'ok', 'message': 'Vous êtes maintenant connecté en tant que ' + username})
        else:
            messages.error(request, 'username ou mot de passe incorrect.')
            return JsonResponse({'status': 'error', 'message': 'username ou mot de passe incorrect.'})
    form = AuthenticationForm()
    return render(request, 'views/login.html', {'form': form})

def register_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		password_confirm = request.POST['password_confirm']
		email = request.POST['email']
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		sexe = request.POST['sexe']
		birthdate = request.POST['birthdate']

		# Valider que les données ne dépassent pas la longueur maximale autorisée
		if len(username) > 50 or len(password) > 50 or len(email) > 50 or len(firstname) > 50 or len(lastname) > 50:
			messages.error(request, 'Les données sont trop longues.')
			return redirect('/register')
		# verifier que le username n'est pas déjà utilisé
		if CustomUser.objects.filter(username=username).exists():
			messages.error(request, 'Ce username est déjà utilisé.')
			return redirect('/register')
		# Valider que l'email n'est pas déjà utilisé
		if CustomUser.objects.filter(email=email).exists():
			messages.error(request, 'Cet email est déjà utilisé.')
			return redirect('/register')
		# verifier que le mot de passe est la confirmation du mot de passe sont identiques
		if password != password_confirm:
			messages.error(request, 'Les mots de passe ne correspondent pas.')
			return redirect('/register')
		# Valider que le mot de passe contient au moins 8 caractères
		if len(password) < 8:
			messages.error(request, 'Le mot de passe doit contenir au moins 8 caractères.')
			return redirect('/register')
		# verifier que la date de naissance est valide
		try:
			birthdate = timezone.datetime.strptime(birthdate, '%Y-%m-%d').replace(tzinfo=pytz.UTC)
		except ValueError:
			messages.error(request, 'La date de naissance est invalide.')
			return redirect('/register')
		#verifier que la date de naissance n'est pas dans le futur
		if birthdate > timezone.now():
			messages.error(request, 'La date de naissance est dans le futur.')
			return redirect('/register')

		# Créer l'utilisateur
		user = CustomUser.objects.create(username=username, password=make_password(password), email=email, first_name=firstname, last_name=lastname ,sexe=sexe, birthdate=birthdate, date_joined=timezone.now())
		messages.success(request, 'Votre compte a été créé avec succès.')
		return redirect('/login')
	else:
		formregister = UserCreationForm()
		return render(request, 'views/register.html', {'form': formregister})

def games(request):
	if request.accepts("text/html"):
		return render(request, 'views/games.html')
	elif request.accepts("application/json"):
		 return JsonResponse({'status': 'ok', 'message': 'Hello'})
	return render(request, 'views/games.html')

def game(request):
	return render(request, 'views/game.html')

def pong(request):
	return render(request, 'views/games/pong.html')

def shooter(request):
	return render(request, 'views/games/shooter.html')
