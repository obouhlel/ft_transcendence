from django.http import JsonResponse
from django.contrib.auth import logout as django_logout
from django.views.decorators.http import require_http_methods

@require_http_methods(['POST'])
def logout_user(request):
	user = request.user
	user.status = 'offline'
	user.save()
	django_logout(request)
	return JsonResponse({'status': 'ok', 'message': 'You are now logged out.'})
