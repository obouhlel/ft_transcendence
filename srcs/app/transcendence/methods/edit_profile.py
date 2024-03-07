from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as django_login
from django.utils import timezone
from transcendence.models  import CustomUser
import pytz

@require_http_methods(['POST'])
def edit_profile(request):
	data = request.POST
	try:
		user = CustomUser.objects.get(username=request.user.username)
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)

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
	sexe = data.get('sexe', user.sexe)
	if sexe:
		user.sexe = data.get('sexe', user.sexe)

	birthdate = data.get('birthdate')
	if birthdate:
		try:
			birthdate = timezone.datetime.strptime(birthdate, '%Y-%m-%d').replace(tzinfo=pytz.UTC)
			if birthdate > timezone.now():
				return JsonResponse({'status': 'error', 'message': 'The birthdate is in the future.'}, status=400)
			user.birthdate = birthdate
		except ValueError:
			return JsonResponse({'status': 'error', 'message': 'Invalid birthdate.'}, status=400)

	if 'avatar' in request.FILES:
		avatar_file = request.FILES['avatar']
		if avatar_file.size > 1024 * 1024:
			return JsonResponse({'status': 'error', 'message': 'Image is too large. (Max 1MB)'}, status=400)
		if user.avatar:
			user.avatar.delete()
		user.avatar = avatar_file

	password = data.get('password')
	password_confirm = data.get('password_confirm')
	if password and password_confirm:
		if password != password_confirm:
			return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'}, status=400)
		if len(password) < 8:
			return JsonResponse({'status': 'error', 'message': 'Password must be at least 8 characters long.'}, status=400)
		user.password = make_password(password)  # Fix: Use user.password instead of reassigning user

	user.save()
	authenticate(request, username=user.username, password=password)
	django_login(request, user)
	return JsonResponse({'status': 'ok', 'message': 'Your profile has been successfully updated!'})
