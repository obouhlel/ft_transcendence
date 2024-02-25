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

#return data as friend request object
@login_required
@require_http_methods(['GET'])
def getAllFriendRequest(request):
	try:
		list_friend_request = request.user.friend_request.all()
		data = [request.friend_request_data() for request in list_friend_request]
		return JsonResponse({'status': 'ok', 'friend_request': data})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)

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


#return data as friend request object
@login_required
@require_http_methods(['GET'])
def getAllFriendRequestSentByUser(request):
	try:
		list_friend_request = request.user.friend_request_sent.all()
		data = [request.friend_request_data() for request in list_friend_request]
		return JsonResponse({'status': 'ok', 'friend_request': data})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)

@login_required
@require_http_methods(['GET'])
def getAllFriendRequestSentByUser(request, id_user):
	try:
		user = CustomUser.objects.get(id=id_user)
		list_friend_request = user.friend_request_sent.all()
		data = [request.friend_request_data() for request in list_friend_request]
		return JsonResponse({'status': 'ok', 'friend_request': data})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)




# friend_requests
# POST: SEND FRIEND REQUEST
# PARAMS: friend_id
# FORMATS:
@login_required
@require_http_methods(['POST'])
def send_friend_request(request):
	data = json.loads(request.body)
	friend_id = data['user_id']
	user = request.user
	try:
		friend = CustomUser.objects.get(id=friend_id)
		if friend == user:
			return JsonResponse({'status': 'error', 'message': 'You can\'t send a friend request to yourself.'}, status=400)
		if friend in user.friends.all():
			return JsonResponse({'status': 'error', 'message': 'You are already friend with this user.'}, status=400)
		if friend in user.friend_requests.all():
			return JsonResponse({'status': 'error', 'message': 'You already sent a friend request to this user.'}, status=400)
		if user in friend.friend_requests.all():
			return JsonResponse({'status': 'error', 'message': 'This user already sent you a friend request, please accept it.'}, status=400)
		user.request_sent.create(sender=user, receiver=friend, date=timezone.now())
		friend.request_received.create(sender=user, receiver=friend, date=timezone.now())
		#sent notification to the user friend
		return JsonResponse({'status': 'ok', 'message': 'Friend Request sent successfully.'})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)
	
#---------------------------------#
	
def accept_friend_request(sender, receiver):
	sender.friends.add(receiver)
	receiver.friends.add(sender)
	sender.request_sent.get(sender=sender, receiver=receiver).delete()
	receiver.request_received.get(sender=sender, receiver=receiver).delete()
	sender.save()
	receiver.save()

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
