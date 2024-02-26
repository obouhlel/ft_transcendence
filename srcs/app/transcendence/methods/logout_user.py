from django.http import JsonResponse
from django.contrib.auth import logout as django_logout

def logout_user(request):
	django_logout(request)
	user = request.user
	user.status = 'offline'
	user.save()
	return JsonResponse({'status': 'ok', 'message': 'You are now logged out.'})
