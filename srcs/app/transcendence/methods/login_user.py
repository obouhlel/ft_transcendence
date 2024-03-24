from django.http import JsonResponse
from django.contrib.auth import authenticate, login as django_login
from django.views.decorators.http import require_http_methods
import json

import logging
logger = logging.getLogger(__name__)

@require_http_methods(['POST'])
def login_user(request):
	data = json.loads(request.body)
	username = data['username']
	if not username:
		return JsonResponse({'status': 'error', 'message': 'Username is required.'}, status=400)
	password = data['password']
	if not password:
		return JsonResponse({'status': 'error', 'message': 'Password is required.'}, status=400)
	
	user = authenticate(request, username=username, password=password)
	if user is not None and user.status == 'Online':
		return JsonResponse({'status': 'error', 'message': 'User is already logged in.'}, status=400)
	if user is not None:
		django_login(request, user)
		return JsonResponse({'status': 'ok', 'message': 'You are now logged in as ' + username})
	else:
		return JsonResponse({'status': 'error', 'message': 'Incorrect username or password.'}, status=401)
