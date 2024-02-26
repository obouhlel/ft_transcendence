from django.http import JsonResponse
from django.contrib.auth import authenticate, login as django_login
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(['POST'])
def login_user(request):
	data = json.loads(request.body)
	username = data['username']
	password = data['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		django_login(request, user)
		user.status = 'online'
		return JsonResponse(
			{'status': 'ok', 'message': 'Vous êtes maintenant connecté en tant que ' + username}
		)
	else:
		return JsonResponse(
			{'status': 'error', 'message': 'Nom d\'utilisateur ou mot de passe incorrect.'}, status=401
		)
