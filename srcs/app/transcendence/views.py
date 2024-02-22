from django.http import JsonResponse
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from transcendence.models import CustomUser
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
import json
import pytz

def index(request):
	return render(request, 'index.html')

def page(request, page):
	# tableau avec les pages autorisées
	allowed_pages = ['home', 'welcome', 'login', 'register', 'profile', 'edit_profile', 'games', 'game', 'pong', 'shooter', '']
	if page not in allowed_pages:
		return JsonResponse({'status': 'error', 'page': 'page inconnue.'}, status=404)
	elif page == '' or page == 'home':
		html_content = render_to_string('home.html', request=request)
	elif ((page == 'login' or page == 'register') and request.user.is_authenticated):
		html_content = render_to_string('home.html', request=request)
		return JsonResponse({'status': 'error', 'page': html_content, 'message': 'Vous êtes déjà connecté.'}, status=403)
	elif (page != 'login' and page != 'register') and not request.user.is_authenticated:
		html_content = render_to_string('home.html', request=request)
		return JsonResponse({'status': 'error', 'page': html_content, 'message': 'Vous n\'êtes pas connecté.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'Section inconnue.'}, status=404)