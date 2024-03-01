from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Game, Stat_Game, Stat_User_by_Game, Party, friend_request

@ensure_csrf_cookie
def index(request):
	games = Game.objects.all()
	stats = Stat_Game.objects.all()
	stat_user = Stat_User_by_Game.objects.all()
	parties = Party.objects.all()
	friend_requests = friend_request.objects.all()
	return render(request, 'index.html', {'games': games, 'stats': stats, 'stat_user': stat_user, 'parties': parties, 'friend_requests': friend_requests})

def page(request, page):
	games = Game.objects.all()
	stat_user = Stat_User_by_Game.objects.all()
	parties = Party.objects.all()
	context = {'games': games, 'stat_user': stat_user, 'parties': parties}
	allowed_pages = ['login', 'register', 'profile', 'edit_profile', 'games', 'game-1', 'game-2', 'pong', 'shooter']
	error_pages = ['400', '401', '403', '404', '405']
	if page == 'home':
		html_content = render_to_string('home.html', request=request)
		return JsonResponse({'status': 'success', 'page': html_content})
	elif (page == 'login' or page == 'register') and request.user.is_authenticated and page in allowed_pages:
		html_content = render_to_string('error/403.html', request=request)
		return JsonResponse({'status': 'success', 'page': html_content})
	elif (page != 'login' and page != 'register') and not request.user.is_authenticated and page in allowed_pages:
		html_content = render_to_string('error/401.html', request=request)
		return JsonResponse({'status': 'success', 'page': html_content})
	elif page in allowed_pages:
		html_content = render_to_string('views/' + page + '.html', context, request=request)
		return JsonResponse({'status': 'success', 'page': html_content})
	elif page in error_pages:
		html_content = render_to_string('error/' + page + '.html', request=request)
		return JsonResponse({'status': 'success', 'page': html_content})
	else:
		html_content = render_to_string('error/404.html', request=request)
		return JsonResponse({'status': 'success', 'page': html_content})
