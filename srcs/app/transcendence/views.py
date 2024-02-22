from django.http import JsonResponse
from django.template.loader import render_to_string

def page(request, page):
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