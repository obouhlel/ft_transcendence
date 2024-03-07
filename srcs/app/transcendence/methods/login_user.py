from django.http import JsonResponse
from django.contrib.auth import authenticate, login as django_login
from django.views.decorators.http import require_http_methods
import json
import logging
logging = logging.getLogger(__name__)

@require_http_methods(['POST'])
def login_user(request):
	logging.debug(vars(request))
	data = json.loads(request.body)
	username = data['username']
	password = data['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		django_login(request, user)
		user.status = 'Online'
		user.save()
		return JsonResponse(
			{'status': 'ok', 'message': 'You are now logged in as ' + username}
		)
	else:
		return JsonResponse(
			{'status': 'error', 'message': 'Incorrect username or password.'}, status=401
		)
