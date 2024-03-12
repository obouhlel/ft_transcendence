from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from transcendence.models  import CustomUser, FriendRequest
# from transcendence.consumers import send_notification
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


def user1_sent_request_to_user2(user1, user2):
	for f in user1.sender.all():
		if f.receiver == user2:
			return True
	return False

def user1_received_request_from_user2(user1, user2):
	for f in user1.receiver.all():
		if f.sender == user2:
			return True
	return False



# friend_requests
# POST: SEND FRIEND REQUEST
# PARAMS: friend_id
# FORMATS:
@login_required
@require_http_methods(['POST'])
def sendFriendRequest(request):
	data = json.loads(request.body)
	friend_id = data['id_user']
	user = request.user
	try:
		friend = CustomUser.objects.get(id=friend_id)
		if friend == user:
			return JsonResponse({'status': 'error', 'message': 'You can\'t send a friend request to yourself.'}, status=400)
		if friend in user.list_friends.all():
			return JsonResponse({'status': 'error', 'message': 'You are already friend with this user.'}, status=400)
		if user1_sent_request_to_user2(user, friend):
			return JsonResponse({'status': 'error', 'message': 'You already sent a friend request to this user.'}, status=400)
		if user1_received_request_from_user2(user, friend):
			return JsonResponse({'status': 'error', 'message': 'You already received a friend request from this user.'}, status=400)
			# accept_friend_request(friend, user)
			# return JsonResponse({'status': 'ok', 'message': 'Friend Request accepted successfully.', 'sender': friend.username, 'receiver': user.username})
		re = FriendRequest.objects.create(sender=user, receiver=friend, created_at=timezone.now())
		#sent notification to the user friend
		# send_notification(friend, "Friend Request", f"{user.username} sent you a friend request.")
		return JsonResponse({'status': 'ok', 'message': 'Friend Request sent successfully.', "request_id": re.id})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)
	
#---------------------------------#

def accept_friend_request(sender, receiver):
	sender.list_friends.add(receiver)
	sender.save()
	x = FriendRequest.objects.filter(sender=sender, receiver=receiver).delete()


# friend_requests
# POST: ACCEPT FRIEND REQUEST OR DECLINE FRIEND REQUEST
# PARAMS: username, action
# FORMATS:
#
@login_required
@require_http_methods(['POST'])
def RespondFriendRequest(request):
	data = json.loads(request.body)
	request_id = data['request_id']
	action = data['action']
	try:
		friend_request = FriendRequest.objects.get(id=request_id)
		sender = friend_request.sender
		# return JsonResponse({'status': 'ok', 'message': 'Friend Request accepted successfully.', 'sender': sender.username, 'receiver': request.user.username})
		if (request.user != friend_request.receiver):
			return JsonResponse({'status': 'error', 'message': 'You can\'t accept or decline a friend request that is not for you.'}, status=400)
		# if(sender == request.user):
		# 	return JsonResponse({'status': 'error', 'message': 'You can\'t accept or decline your own friend request.'}, status=400)
		if sender in request.user.list_friends.all():
			return JsonResponse({'status': 'error', 'message': 'You are already friend with this user.'}, status=400)
		if action != 'accept' and action != 'decline':
			return JsonResponse({'status': 'error', 'message': 'Invalid action.'}, status=400)
		if action == 'accept':
			accept_friend_request(sender, request.user)
			return JsonResponse({'status': 'ok', 'message': 'Friend Request accepted successfully.', 'sender': sender.username, 'receiver': request.user.username})
		elif action == 'decline':
			FriendRequest.objects.filter(sender=sender, receiver=request.user).delete()
			return JsonResponse({'status': 'ok', 'message': 'Friend Request declined successfully.'})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)
	except FriendRequest.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This friend request doesn\'t exist'}, status=404)

#remove friend
# POST: REMOVE FRIEND
# PARAMS: username
@login_required
@require_http_methods(['POST'])
def removeFriend(request):
	data = json.loads(request.body)
	friend_id = data['friend_id']
	try:
		friend = CustomUser.objects.get(id=friend_id)
		if friend == request.user:
			return JsonResponse({'status': 'error', 'message': 'You can\'t remove yourself from your friend list.'}, status=400)
		if friend not in request.user.list_friends.all():
			return JsonResponse({'status': 'error', 'message': 'You are not friend with this user.'}, status=400)
		request.user.list_friends.remove(friend)
		return JsonResponse({'status': 'ok', 'message': 'Friend removed successfully.'})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user doesn\'t exist'}, status=404)


