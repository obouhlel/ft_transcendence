from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from transcendence.models  import CustomUser
import json
from django.utils import timezone

#CRUD : Create, Read, Update, Delete
#Create: POST
#Read: GET
#Update: PUT
#Delete: DELETE


@login_required
@require_http_methods(['GET'])
def getAllFriendRequestofUser(request, id_user):
	try:
		user = CustomUser.objects.get(id=id_user)
		list_friend_request = user.friend_request.all()
		data = [request.friend_request_data() for request in list_friend_request]
		return JsonResponse({'status': 'ok', 'friend_request': data})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)




# friend_requests
# POST: ACCEPT FRIEND REQUEST OR DECLINE FRIEND REQUEST
# PARAMS: username, action
# FORMATS:
#
def respond_to_friend_request(request):
	data = json.loads(request.body)
	username = data['username']
	action = data['action']
	if request.user.is_authenticated:
		if action == 'accept':
			try:
				friend = CustomUser.objects.get(username=username)
				request.user.friend_requests.remove(friend)
				request.user.friends.add(friend)
				return JsonResponse({'status': 'ok', 'message': 'Demande d\'ami acceptée avec succès.'})
			except CustomUser.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)
		elif action == 'decline':
			try:
				friend = CustomUser.objects.get(username=username)
				request.user.friend_requests.remove(friend)
				return JsonResponse({'status': 'ok', 'message': 'Demande d\'ami refusée avec succès.'})
			except CustomUser.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Action inconnue.'}, status=400)
	else:
		return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)

# friend_requests
# GET: RETURN ALL FRIEND REQUESTS
# POST: SEND FRIEND REQUEST
# PARAMS: username, action
# FORMATS:
def request_friend(request):
	data = json.loads(request.body)
	username = data['username']
	action = data['action']
	if request.method == 'GET':
		if request.user.is_authenticated:
			friend_requests = request.user.friend_requests.all()
			data = []
			for friend in friend_requests:
				data += [{
					'username': friend.username,
					'avatar': friend.avatar.url if friend.avatar else None,
				}]
			return JsonResponse({'status': 'ok', 'friend_requests': data})
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	elif request.method == 'POST':
		if request.user.is_authenticated:
			try:
				friend = CustomUser.objects.get(username=username)
				request.user.friend_requests.add(friend)
				return JsonResponse({'status': 'ok', 'message': 'Demande d\'ami envoyée avec succès.'})
			except CustomUser.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)

#remove friend
# POST: REMOVE FRIEND
# PARAMS: username
def remove_friend(request):
	data = json.loads(request.body)
	username = data['username']
	if request.method == 'POST':
		if request.user.is_authenticated:
			try:
				friend = CustomUser.objects.get(username=username)
				request.user.friends.remove(friend)
				return JsonResponse({'status': 'ok', 'message': 'Ami retiré avec succès.'})
			except CustomUser.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)



def is_power_of_two(n):
	return n > 0 and (n & (n - 1)) == 0
