from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from transcendence.models import *

error_pages = ['400', '401', '403', '404', '405']

@ensure_csrf_cookie
def index(request):
	games = Game.objects.all()
	return render(request, 'index.html', {'games': games})

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
		'dashboard'
	]
	games_page = ['pong', 'TicTacToe']
	games = Game.objects.all()
	context = {
		'games': games,
	}
	if page == 'home':
		html_content = render_to_string('home.html', request=request, context=context)
		return JsonResponse({'html': html_content})
	elif (page == 'login' or page == 'register') and request.user.is_authenticated and page in allowed_pages:
		html_content = render_to_string('error/403.html', request=request)
		return JsonResponse({'html': html_content})
	elif (page != 'login' and page != 'register') and not request.user.is_authenticated and page in allowed_pages:
		html_content = render_to_string('error/401.html', request=request)
		return JsonResponse({'html': html_content})
	elif page in games_page:
		html_content = ''
		return JsonResponse({'html': html_content})
	elif page in allowed_pages:
		html_content = render_to_string('views/' + page + '.html', request=request, context=context)
		return JsonResponse({'html': html_content})
	elif page in error_pages:
		html_content = render_to_string('error/' + page + '.html', request=request)
		return JsonResponse({'html': html_content})
	else:
		html_content = render_to_string('error/404.html', request=request)
		return JsonResponse({'html': html_content})
	
def update_header(request, page):
	if page in error_pages:
		html_content = ''
		return JsonResponse({'html': html_content})
	if request.user.is_authenticated:
		notifications = Notification.objects.filter(user=request.user)
	else:
		notifications = []
	context = {
		'notifications': notifications
	}
	html_content = render_to_string('header.html', request=request, context=context)
	return JsonResponse({'html': html_content})