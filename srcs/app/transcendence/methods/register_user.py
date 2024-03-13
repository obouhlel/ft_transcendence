from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from transcendence.models import CustomUser, Stat_User_by_Game, Game
import pytz

@require_http_methods(['POST'])
def register_user(request):
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
		if len(data) > 50:
			return JsonResponse(
				{'status': 'error', 'message': 'Data is too long.'},
				status=400
			)
	if CustomUser.objects.filter(username=username).exists():
		return JsonResponse(
			{'status': 'error', 'message': 'This username is already taken.'},
			status=400
		)
	if CustomUser.objects.filter(email=email).exists():
		return JsonResponse(
			{'status': 'error', 'message': 'This email is already taken.'},
			status=400
		)
	if password != password_confirm:
		return JsonResponse(
			{'status': 'error', 'message': 'Passwords do not match.'},
			status=400
		)
	if len(password) < 8:
		return JsonResponse(
			{'status': 'error', 'message': 'Password must be at least 8 characters long.'},
			status=400
		)
	try:
		birthdate = timezone.datetime.strptime(birthdate, '%Y-%m-%d').replace(tzinfo=pytz.UTC)
	except ValueError:
		return JsonResponse(
			{'status': 'error', 'message': 'Invalid birthdate.'},
			status=400
		)
	if birthdate > timezone.now():
		return JsonResponse(
			{'status': 'error', 'message': 'Birthdate is in the future.'},
			status=400
		)
	if 'avatar' in request.FILES:
		avatar = request.FILES['avatar']
		if avatar.size > 1024 * 1024:
			return JsonResponse(
				{'status': 'error', 'message': 'Image is too large. (Max 1MB). User not created.'},
				status=400
			)

	user = CustomUser.objects.create(
		username=username,
		password=make_password(password),
		email=email,
		first_name=firstname,
		last_name=lastname,
		sexe=sexe,
		birthdate=birthdate,
		date_joined=timezone.now(),
		avatar=avatar
	)
	# delete this if many games or many users
	for game in Game.objects.all():
		Stat_User_by_Game.objects.create(user=user, game=game)
	return JsonResponse({'status': 'ok', 'message': 'Your account has been successfully created.'})