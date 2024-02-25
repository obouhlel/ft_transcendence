from django.http import JsonResponse
from django.contrib.auth import authenticate, login as django_login
import json


def login_user(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		username = data['username']
		password = data['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			django_login(request, user)
			user.status = 'online'
			return JsonResponse({'status': 'ok', 'message': 'Vous êtes maintenant connecté en tant que ' + username})
		else:
			return JsonResponse({'status': 'error', 'message': 'Nom d\'utilisateur ou mot de passe incorrect.'}, status=401)
