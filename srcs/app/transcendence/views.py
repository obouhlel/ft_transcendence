from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.conf import settings

def index(request):
	return render(request, 'index.html')

def page(request, page):
	allowed_pages = ['login', 'register', 'profile', 'edit_profile', 'games', 'game-1', 'game-2', 'pong', 'shooter']
	settings.LOGGER.debug('page: ' + page)
	if page == 'home':
		html_content = render_to_string('home.html', request=request)
		return JsonResponse({'status': 'success', 'page': html_content})
	elif ((page == 'login' or page == 'register') and request.user.is_authenticated):
		html_content = render_to_string('home.html', request=request)
		return JsonResponse({'status': 'error', 'page': html_content, 'message': 'Vous êtes déjà connecté.'}, status=403)
	elif (page != 'login' and page != 'register') and not request.user.is_authenticated:
		html_content = render_to_string('home.html', request=request)
		return JsonResponse({'status': 'error', 'page': html_content, 'message': 'Vous n\'êtes pas connecté.'}, status=401)
	elif page in allowed_pages:
		html_content = render_to_string('views/' + page + '.html', request=request)
		return JsonResponse({'status': 'success', 'page': html_content})
	else:
		return JsonResponse({'status': 'error', 'page': 'Page not found'}, status=404)
