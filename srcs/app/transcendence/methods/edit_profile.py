from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as django_login
from transcendence.models  import CustomUser

@require_http_methods(['POST'])
def edit_profile(request):
	data = request.POST
	try:
		user = CustomUser.objects.get(username=request.user.username)
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)

	password = data.get('password')
	if not check_password(password, request.user.password):
		return JsonResponse({'status': 'error', 'message': 'Incorrect password.'}, status=400)

	username = data.get('username')
	if username and username != user.username:
		if CustomUser.objects.filter(username=username).exists():
			return JsonResponse({'status': 'error', 'message': 'This username is already taken.'}, status=400)
		user.username = username

	email = data.get('email')
	if email and email != user.email:
		if CustomUser.objects.filter(email=email).exists():
			return JsonResponse({'status': 'error', 'message': 'This email is already taken.'}, status=400)
		user.email = email

	first_name = data.get('firstname', user.first_name)
	if first_name:
		user.first_name = first_name

	last_name = data.get('lastname', user.last_name)
	if last_name:
		user.last_name = last_name

	if 'avatar' in request.FILES:
		avatar_file = request.FILES['avatar']
		if avatar_file.size > 24 * 1024:
			return JsonResponse({'status': 'error', 'message': 'Image is too large. (Max 1MB)'}, status=400)
		if user.avatar:
			user.avatar.delete()
		user.avatar = avatar_file
	
	user.save()
	authenticate(request, username=user.username, password=password)
	django_login(request, user)
	return JsonResponse({'status': 'ok', 'message': 'Your profile has been successfully updated!'})

@require_http_methods(['POST'])
def change_password(request):
	data = request.POST
	try:
		user = CustomUser.objects.get(username=request.user.username)
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)

	password = data.get('old_password')
	if not check_password(password, request.user.password):
		return JsonResponse({'status': 'error', 'message': 'Incorrect password.'}, status=400)

	new_password = data.get('new_password')
	if not new_password:
		return JsonResponse({'status': 'error', 'message': 'New password is required.'}, status=400)
	elif len(new_password) < 8:
		return JsonResponse({'status': 'error', 'message': 'Password must be at least 8 characters long.'}, status=400)
	
	confirm_password = data.get('confirm_password')
	if new_password != confirm_password:
		return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'}, status=400)

	user.set_password(new_password)
	user.save()
	authenticate(request, username=user.username, password=new_password)
	django_login(request, user)
	return JsonResponse({'status': 'ok', 'message': 'Your password has been successfully updated!'}, status=200)
