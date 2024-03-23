from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from transcendence.models  import CustomUser
from django.db.models import Q # permet de faire des requetes plus complexes (AND, OR, NOT)

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

#---------------------------------ADD FRIEND---------------------------------#
@login_required
@require_http_methods(['POST'])
def addFriend(request, id_user):
	if request.user.id == id_user:
		return JsonResponse({'status': 'error', 'message': 'You cannot add yourself as a friend.'}, status=400)
	try:
		friend_to_add = CustomUser.objects.get(id=id_user)
		if friend_to_add in request.user.list_friends.all():
			return JsonResponse({'status': 'error', 'message': 'This user is already your friend.'}, status=400)
		request.user.list_friends.add(friend_to_add)
		return JsonResponse({'status': 'ok', 'message': 'Friend added successfully.'})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)

#---------------------------------DELETE FRIEND---------------------------------#

@login_required
@require_http_methods(['DELETE'])
def deleteFriend(request, id_user):
	try:
		friend_to_delete = CustomUser.objects.get(id=id_user)
		if friend_to_delete not in request.user.list_friends.all():
			return JsonResponse({'status': 'error', 'message': 'This user is not your friend.'}, status=400)
		request.user.list_friends.remove(friend_to_delete)
		return JsonResponse({'status': 'ok', 'message': 'Friend deleted successfully.'})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)

#---------------------------------GET FRIEND REQUEST---------------------------------#
@login_required
@require_http_methods(['GET'])
def getFriendRequest(request):
    data = [friend_request.friend_request_data() for friend_request in request.user.receiver.filter(status='waiting')]
    return JsonResponse({'status': 'ok', 'friend_requests': data})

#---------------------------------SEND FRIEND REQUEST---------------------------------#
@login_required
@require_http_methods(['POST'])
def sendFriendRequest(request, id_user):
	if request.user.id == id_user:
		return JsonResponse({'status': 'error', 'message': 'You cannot send a friend request to yourself.'}, status=400)
	try:
		friend_to_add = CustomUser.objects.get(id=id_user)
		if friend_to_add in request.user.list_friends.all():
			return JsonResponse({'status': 'error', 'message': 'This user is already your friend.'}, status=400)
		if friend_to_add in request.user.list_friend_requests.all():
			return JsonResponse({'status': 'error', 'message': 'You have already sent a friend request to this user.'}, status=400)
		request.user.list_friend_requests.add(friend_to_add)
		return JsonResponse({'status': 'ok', 'message': 'Friend request sent successfully.'})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)

#---------------------------------ACCEPT FRIEND REQUEST---------------------------------#
@login_required
@require_http_methods(['POST'])
def acceptFriendRequest(request, id_user):
	try:
		friend_to_accept = CustomUser.objects.get(id=id_user)
		if friend_to_accept not in request.user.list_friend_requests.all():
			return JsonResponse({'status': 'error', 'message': 'This user has not sent you a friend request.'}, status=400)
		request.user.list_friend_requests.remove(friend_to_accept)
		request.user.list_friends.add(friend_to_accept)
		return JsonResponse({'status': 'ok', 'message': 'Friend request accepted successfully.'})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)

#---------------------------------DELETE FRIEND REQUEST---------------------------------#
@login_required
@require_http_methods(['DELETE'])
def deleteFriendRequest(request, id_user):
	try:
		friend_to_delete = CustomUser.objects.get(id=id_user)
		if friend_to_delete not in request.user.list_friend_requests.all():
			return JsonResponse({'status': 'error', 'message': 'This user has not sent you a friend request.'}, status=400)
		request.user.list_friend_requests.remove(friend_to_delete)
		return JsonResponse({'status': 'ok', 'message': 'Friend request deleted successfully.'})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)
