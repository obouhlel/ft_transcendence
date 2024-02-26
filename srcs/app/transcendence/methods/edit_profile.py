from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from transcendence.models  import CustomUser
from django.views.decorators.csrf import csrf_exempt
import pytz

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
