import json
import pytz
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from transcendence.models import CustomUser
from django.conf import settings
from django.shortcuts import redirect
import requests
from django.core.files.base import ContentFile
import logging
logger = logging.getLogger(__name__)

def login_42(request):
	if request.method == 'GET':
		code = request.GET.get('code')
		if code:
			token_url = 'https://api.intra.42.fr/oauth/token'

			client_id = settings.API_42_UID
			secret_key = settings.API_42_SECRET
			redirect_uri = settings.API_42_REDIRECT_URI.replace('$HOST', request.get_host())
			logger.log(logging.DEBUG, 'redirect_uri: ' + redirect_uri)

			data = {
				'grant_type': 'authorization_code',
				'client_id': client_id,
				'client_secret': secret_key,
				'code': code,
				'redirect_uri': redirect_uri,
			}
			logger.log(logging.DEBUG, 'data: ' + json.dumps(data))
			response = requests.post(token_url, data=data)
			if response.status_code == 200:
				access_token = response.json()['access_token']
				token_type = response.json()['token_type']
				user_url = 'https://api.intra.42.fr/v2/me'
				headers = {
					'Authorization': token_type + ' ' + access_token,
				}
				response = requests.get(user_url, headers=headers)
				if response.status_code == 200:
					user_data = response.json()
					username = user_data['login']
					email = user_data['email']
					firstname = user_data['first_name']
					lastname = user_data['last_name']
					avatar_url = user_data.get('image', {}).get('link')
					response = requests.get(avatar_url)
				if response.status_code == 200:
					avatar_file = ContentFile(response.content)
					avatar_file.name = username + '.jpg'
					if CustomUser.objects.filter(token=access_token).exists():
						user = CustomUser.objects.get(username=username)
						django_login(request, user)
						return redirect('/')
					else:
						if CustomUser.objects.filter(username=username).exists():
							return JsonResponse({'status': 'error', 'message': 'Ce username est déjà utilisé.'}, status=400)
						user = CustomUser.objects.create(username=username, email=email, first_name=firstname, last_name=lastname, avatar=avatar_file, token=access_token, date_joined=timezone.now())
						django_login(request, user)
						return redirect('/')
				else:
					return JsonResponse({'status': 'error', 'message': 'Impossible de récupérer les données de l\'utilisateur.'}, status=400)
			else:
				logger.log(logging.ERROR, response.json())
				return JsonResponse({'status': 'error', 'message': 'Impossible de récupérer le token d\'accès.'}, status=400)
		else:
			return JsonResponse({'status': 'error', 'message': 'Code invalide.'}, status=400)
	else:
		return JsonResponse({'status': 'error', 'message': 'Cette méthode n\'est pas autorisée.'}, status=405)
