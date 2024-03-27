from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as django_login
from django.utils import timezone
from django.core.files.base import ContentFile
from transcendence.models import CustomUser, Stat_User_by_Game, Game
import re
import pytz
import requests

@require_http_methods(['POST'])
def register_42(request):
	data = request.POST
	username = data.get('username')
	password = data.get('password')
	password_confirm = data.get('password_confirm')
	email = data.get('email')
	firstname = data.get('firstname')
	lastname = data.get('lastname')
	sexe = data.get('sexe')
	birthdate = data.get('birthdate')
	data_list = [username, password, email, firstname, lastname]

	for data in data_list:
		if data is None or data == '':
			return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)
	
	if not birthdate:
		return JsonResponse({'status': 'error', 'message': 'Birthdate is required.'}, status=400)

	if not re.match('^[a-zA-Z0-9_-]{3,20}$', username):
		return JsonResponse({'status': 'error', 'message': 'Invalid username. Use only alphanumeric characters, dashes and underscores. Length must be between 3 and 20 characters.'}, status=400)

	if not re.match('^[a-zA-Z0-9_-]{3,20}$', firstname):
		return JsonResponse({'status': 'error', 'message': 'Invalid first name. Use only alphanumeric characters, dashes and underscores. Length must be between 3 and 20 characters.'}, status=400)

	if not re.match('^[a-zA-Z0-9_-]{3,20}$', lastname):
		return JsonResponse({'status': 'error', 'message': 'Invalid last name. Use only alphanumeric characters, dashes and underscores. Length must be between 3 and 20 characters.'}, status=400)

	if not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
		return JsonResponse({'status': 'error', 'message': 'Invalid email address.'}, status=400)

	for data in data_list:
		if len(data) > 50:
			return JsonResponse({'status': 'error', 'message': 'Data is too long.'}, status=400)

	if CustomUser.objects.filter(username=username).exists():
		return JsonResponse({'status': 'error', 'message': 'This username is already taken.'}, status=400)

	if CustomUser.objects.filter(email=email).exists():
		return JsonResponse({'status': 'error', 'message': 'This email is already taken.'}, status=400)

	if password != password_confirm:
		return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'}, status=400)

	if len(password) < 8:
		return JsonResponse({'status': 'error', 'message': 'Password must be at least 8 characters long.'},	status=400)

	try:
		birthdate = timezone.datetime.strptime(birthdate, '%Y-%m-%d').replace(tzinfo=pytz.UTC)
	except ValueError:
		return JsonResponse({'status': 'error', 'message': 'Invalid birthdate.'}, status=400)

	if birthdate > timezone.now():
		return JsonResponse({'status': 'error', 'message': 'Birthdate is in the future.'}, status=400)

	avatar = None
	if 'avatar' in request.FILES:
		avatar = request.FILES['avatar']
		if not avatar.content_type.startswith('image'):
			return JsonResponse({'status': 'error', 'message': 'Avatar must be an image.'}, status=400)
		if avatar.size > 2 * 1024 * 1024:
			return JsonResponse({'status': 'error', 'message': 'Avatar is too big.'}, status=400)
	else:
		avatar_url = request.session.pop('avatar')
		avatar = ContentFile(requests.get(avatar_url).content, 'avatar.jpg')
	
	user = CustomUser.objects.create(
		username=username,
		password=make_password(password),
		email=email,
		first_name=firstname,
		last_name=lastname,
		sexe=sexe,
		birthdate=birthdate,
		avatar=avatar,
		date_joined=timezone.now(),
		token=request.session.get('token')
	)
	for game in Game.objects.all():
		Stat_User_by_Game.objects.create(user=user, game=game)
	request.session.pop('token')
	user.save()
	authenticate(request, username=username, password=password)
	django_login(request, user)
	return JsonResponse({'status': 'ok', 'message': 'Your account has been successfully created.'})