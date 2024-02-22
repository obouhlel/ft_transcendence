from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

def index(request):
	return render(request, 'index.html')

def page(request, page):
	allowed_pages = ['home', 'login', 'register', 'profile', 'edit_profile', 'games', 'game', 'pong', 'shooter', '']
	if page not in allowed_pages:
		return JsonResponse({'status': 'error', 'page': 'Page not found'}, status=404)
	elif page == '' or page == 'home':
		html_content = render_to_string('home.html', request=request)
		return JsonResponse({'status': 'success', 'page': html_content})
	elif ((page == 'login' or page == 'register') and request.user.is_authenticated):
		html_content = render_to_string('home.html', request=request)
		return JsonResponse({'status': 'error', 'page': html_content, 'message': 'Vous êtes déjà connecté.'}, status=403)
	elif (page != 'login' and page != 'register') and not request.user.is_authenticated:
		html_content = render_to_string('home.html', request=request)
		return JsonResponse({'status': 'error', 'page': html_content, 'message': 'Vous n\'êtes pas connecté.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'Section inconnue.'}, status=404)