from django.shortcuts import render
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as django_login
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
import pytz
import json

# Create your views here.
def login(request):
	if request.method == 'POST':
		print("Request body: ", request.body)
		data = json.loads(request.body)
		username = data.get('username')
		password = data.get('password')
		print("Username: ", username)
		print("Password: ", password)
		user = authenticate(request, username=username, password=password)
		print("Authentication result: ", user)
		if user is not None:
			django_login(request, user)
			messages.success(request, 'Vous êtes maintenant connecté.')
			return redirect('/pong')  # Remplacez '/home' par l'URL de la page vers laquelle vous souhaitez rediriger l'utilisateur après la connexion
		else:
			messages.error(request, 'username ou mot de passe incorrect.')
			return redirect('/login')
	else:
		return render(request, 'views/login.html')

def signin(request):
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
			return redirect('/signin')
		# verifier que le username n'est pas déjà utilisé
		if User.objects.filter(username=username).exists():
			messages.error(request, 'Ce username est déjà utilisé.')
			return redirect('/signin')
		# Valider que l'email n'est pas déjà utilisé
		if User.objects.filter(email=email).exists():
			messages.error(request, 'Cet email est déjà utilisé.')
			return redirect('/signin')
		# verifier que le mot de passe est la confirmation du mot de passe sont identiques
		if password != password_confirm:
			messages.error(request, 'Les mots de passe ne correspondent pas.')
			return redirect('/signin')
		# Valider que le mot de passe contient au moins 8 caractères
		if len(password) < 8:
			messages.error(request, 'Le mot de passe doit contenir au moins 8 caractères.')
			return redirect('/signin')
		# verifier que la date de naissance est valide
		try:
			birthdate = timezone.datetime.strptime(birthdate, '%Y-%m-%d').replace(tzinfo=pytz.UTC)
		except ValueError:
			messages.error(request, 'La date de naissance est invalide.')
			return redirect('/signin')
		#verifier que la date de naissance n'est pas dans le futur
		if birthdate > timezone.now():
			messages.error(request, 'La date de naissance est dans le futur.')
			return redirect('/signin')

		# Créer l'utilisateur
		user = User.objects.create(username=username, password=make_password(password), email=email, firstname=firstname, lastname=lastname ,sexe=sexe, birthdate=birthdate, date_creation=timezone.now())
		messages.success(request, 'Votre compte a été créé avec succès.')
		return redirect('/login')
	else:
		return render(request, 'views/signin.html')

def games(request):
	return render(request, 'views/games.html')

def pong(request):
	return render(request, 'views/games/pong.html')

def pew(request):
	return render(request, 'views/games/pew.html')
