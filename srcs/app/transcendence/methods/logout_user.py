from django.http import JsonResponse
from django.contrib.auth import logout as django_logout

def logout_user(request):
	django_logout(request)
	return JsonResponse({'status': 'ok', 'message': 'Vous êtes maintenant déconnecté.'})
