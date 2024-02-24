from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from transcendence.models import CustomUser
import json



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
