from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from transcendence.models  import CustomUser

#---------------------------------GET FRIEND---------------------------------#
@login_required
@require_http_methods(['GET'])
def getAllFriendsofUser(request, id_user):
	try:
		user = CustomUser.objects.get(id=id_user)
		data = user.getFriends()
		return JsonResponse({'status': 'ok', 'friends': data})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)