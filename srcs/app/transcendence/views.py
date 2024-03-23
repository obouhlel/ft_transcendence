from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from transcendence.models import *
from django.conf import settings
from logging import getLogger

error_pages = ['400', '401', '403', '404', '405']
allowed_pages = ['login', 'register', 'register-42', 'profile', 'edit_profile', 'change-password',
				'games', 'game-1', 'game-2', 'join-tournament',
				'create-tournament', 'lobby-tournament', 'dashboard', 'game-info']
games_pages = ['pong', 'tictactoe']

logger = getLogger(__name__)

@ensure_csrf_cookie
def index(request):
	games = Game.objects.all()
	return render(request, 'index.html', {'games': games})

def page(request, page):
	games = Game.objects.all()
	context = {
		'games': games,
	}
	logger.debug('page: ' + page)
	if request.user.is_authenticated:
		request.user.update_status('Online')
	if page == 'home':
		html_content = render_to_string('home.html', request=request, context=context)
		return JsonResponse({'html': html_content})
	if page == 'game' and request.user.is_authenticated:
		try:
			id = request.GET.get('id')
			if not id:
				raise Exception
			game = Game.objects.get(id = id)
			html_content = render_to_string('views/game.html', request=request, context={'game': game})
			return JsonResponse({'html': html_content})
		except:
			html_content = render_to_string('error/404.html', request=request)
			return JsonResponse({'html': html_content})
	if page == 'tournament' and request.user.is_authenticated:
		try:
			id = request.GET.get('id')
			if not id:
				raise Exception
			game = Game.objects.get(id = id)
			tournaments = Tournament.objects.filter(game=game, status='waiting')
			user = request.user
			if user.tournaments.filter(game=game, status='waiting').count() > 0:
				current_tournament = user.tournaments.filter(game=game, status='waiting').first()
			else:
				current_tournament = None
			html_content = render_to_string('views/tournament.html', request=request, context={'tournaments': tournaments, 'game': game, 'user': user, 'current_tournament': current_tournament})
			return JsonResponse({'html': html_content})
		except game.DoesNotExist:
			logger.error(e)
			html_content = render_to_string('error/404.html', request=request)
			return JsonResponse({'html': html_content})
	if page == 'lobby-tournament' and request.user.is_authenticated:
		try:
			id = request.GET.get('id')
			if not id:
				raise Exception
			tournament = Tournament.objects.get(id = id).tournament_data()
			html_content = render_to_string('views/lobby-tournament.html', request=request, context={'tournament': tournament})
			return JsonResponse({'html': html_content})
		except Exception as e:
			logger.error(e)
			html_content = render_to_string('error/404.html', request=request)
			return JsonResponse({'html': html_content})
	if page == 'create-tournament' and request.user.is_authenticated:
		try:
			id = request.GET.get('id')
			if not id:
				raise Exception
			user = request.user
			game = Game.objects.get(id = id)
			html_content = render_to_string('views/create-tournament.html', request=request, context={'game': game, 'user': user})
			return JsonResponse({'html': html_content})
		except:
			html_content = render_to_string('error/404.html', request=request)
			return JsonResponse({'html': html_content})	
	elif (page == 'login' or page == 'register' or page == 'register-42') and request.user.is_authenticated and page in allowed_pages:
		html_content = render_to_string('error/403.html', request=request)
		return JsonResponse({'html': html_content})
	elif (page != 'login' and page != 'register' and page != 'register-42') and not request.user.is_authenticated and page in allowed_pages:
		html_content = render_to_string('error/401.html', request=request)
		return JsonResponse({'html': html_content})
	elif page in games_pages:
		if request.user.is_authenticated:
			request.user.update_status('In Game')
		user_id = request.user.id
		party = Party.objects.filter(player1=user_id, status='Waiting').first()
		if not party:
			party = Party.objects.filter(player2=user_id, status='Waiting').first()
		if party:
			player1 = CustomUser.objects.get(id=party.player1.id)
			player2 = CustomUser.objects.get(id=party.player2.id)
			context = {
				'party': party,
				'player1': player1,
				'player2': player2,
				'game': page
			}
		html_content = render_to_string('views/game-info.html', request=request, context=context)
		return JsonResponse({'html': html_content})
	elif page == 'register-42' and not request.user.is_authenticated:
		try:
			data = request.session.get('data')
			context = { 'data': data }
			token = data.get('token')
			html_content = render_to_string('views/register-42.html', context, request=request)
			request.session.pop('data')
			request.session['token'] = token
			return JsonResponse({'html': html_content})
		except:
			html_content = render_to_string('error/404.html', request=request)
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
	notifications = []
	if request.user.is_authenticated:
		pending = FriendRequest.objects.filter(receiver=request.user)
		for p in pending:
			notifications.append(p.friend_request_data())
	context = {
		'notifications': notifications,
		'page': page
	}
	html_content = render_to_string('header.html', request=request, context=context)
	return JsonResponse({'html': html_content})
	
def config(request):
	return render(request, 'config.js', content_type='application/javascript', context={'CLIENT_ID': settings.API_42_UID})
