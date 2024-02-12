# views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse

def index(request):
	return render(request, 'index.html')

def section(request, section):
	if section == 'home':
		return HttpResponse(render_to_string('home.html', request=request))
	elif section == 'login':
		return HttpResponse(render_to_string('views/login.html', request=request))
	elif section == 'logout':
		return JsonResponse({'message': 'Deconnexion en cours..'})
	elif section == 'register':
		return HttpResponse(render_to_string('views/register.html', request=request))
	elif section == 'profile':
		return HttpResponse(render_to_string('views/profile.html', request=request))
	elif section == 'edit_profile':
		return HttpResponse(render_to_string('views/edit_profile.html', request=request))
	elif section == 'games':
		return HttpResponse(render_to_string('views/games.html', request=request))
	elif section == 'game':
		return HttpResponse(render_to_string('views/game.html', request=request))
	elif section == 'pong':
		return HttpResponse(render_to_string('views/pong.html', request=request))
	elif section == 'shooter':
		return HttpResponse(render_to_string('views/shooter.html', request=request))
	else:
		return JsonResponse({'status': 'error', 'message': 'Section inconnue.'}, status=404)

