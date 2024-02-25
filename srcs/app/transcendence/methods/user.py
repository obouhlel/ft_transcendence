
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from transcendence.models  import CustomUser

#CRUD : Create, Read, Update, Delete
#Create: POST : Create a new user
#Read: GET : Get a user information by id or by name
#Update: PUT : Update a user information
#Delete: DELETE : Delete a user
# -------------------------------GET USER-----------------------------#
@login_required
@require_http_methods(['GET'])
def getUserName(request):
	return JsonResponse({'username': request.user.username})

@login_required
@require_http_methods(['GET'])
def getUserByName(request, username):
	try:
		user = CustomUser.objects.get(username=username)
		data = user.user_data()
		return JsonResponse({'status': 'ok', 'user': data})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)

@login_required
@require_http_methods(['GET'])
def getUserById(request, id):
	try:
		user = CustomUser.objects.get(id=id)
		data = user.user_data()
		return JsonResponse({'status': 'ok', 'user': data})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)

@login_required
@require_http_methods(['GET'])
def getUserByStatus(request, status):
	users = CustomUser.objects.filter(status=status)
	data = [user.user_data() for user in users]
	return JsonResponse({'status': 'ok', 'users': data})

@login_required
@require_http_methods(['GET'])
def getAllUsers(request):
	users = CustomUser.objects.all()
	data = []
	for user in users:
		data += [user.user_data()]
	return JsonResponse({'status': 'ok', 'users': data})


@login_required
@require_http_methods(['GET'])
def getFriends(request):
	user = request.user
	friends = user.friends.all()
	data = [friend.user_data() for friend in friends]
	return JsonResponse({'status': 'ok', 'friends': data})

@login_required
@require_http_methods(['GET'])
def getOnlineFriends(request):
	user = request.user
	friends = user.friends.filter(status='online')
	data = [friend.user_data() for friend in friends]
	return JsonResponse({'status': 'ok', 'friends': data})

@login_required
@require_http_methods(['GET'])
def getOfflineFriends(request):
	user = request.user
	friends = user.friends.filter(status='offline')
	data = [friend.user_data() for friend in friends]
	return JsonResponse({'status': 'ok', 'friends': data})



# -------------------------------POST USER-----------------------------#
#=> register_user.py

# -------------------------------PUT USER-----------------------------#
#=> edit_profile.py

# -------------------------------DELETE USER-----------------------------#
#not implemented
	