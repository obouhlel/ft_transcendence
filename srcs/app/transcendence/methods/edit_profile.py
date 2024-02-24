from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from transcendence.models  import CustomUser
from django.views.decorators.csrf import csrf_exempt
import json


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
