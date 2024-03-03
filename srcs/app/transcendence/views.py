from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from transcendence.models import *

@ensure_csrf_cookie
def index(request):
	return render(request, 'index.html')

def page(request, page):
	allowed_pages = [
		'login',
		'register',
		'profile',
		'edit_profile',
		'games',
		'game-1',
		'game-2',
		'join-tournament',
		'create-tournament',
		'lobby-tournament',
		'pong',
		'TicTacToe',
	]
	error_pages = ['400', '401', '403', '404', '405']
	games = Game.objects.all()
	if page == 'home':
		html_content = render_to_string('home.html', request=request, context={'games': games,'notifications': [] if request.user.is_anonymous else request.user.get_notifications()})
		return JsonResponse({'page': html_content})
	elif (page == 'login' or page == 'register') and request.user.is_authenticated and page in allowed_pages:
		html_content = render_to_string('error/403.html', request=request)
		return JsonResponse({'page': html_content})
	elif (page != 'login' and page != 'register') and not request.user.is_authenticated and page in allowed_pages:
		html_content = render_to_string('error/401.html', request=request)
		return JsonResponse({'page': html_content})
	elif page in allowed_pages:
		html_content = render_to_string('views/' + page + '.html', request=request, context={'games': games})
		return JsonResponse({'page': html_content})
	elif page in error_pages:
		html_content = render_to_string('error/' + page + '.html', request=request)
		return JsonResponse({'page': html_content})
	else:
		html_content = render_to_string('error/404.html', request=request)
		return JsonResponse({'page': html_content})
