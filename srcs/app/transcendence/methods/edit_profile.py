from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_http_methods
from transcendence.models import CustomUser
import re
import logging

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
def edit_profile(request):
	data = request.POST
	username = data.get("username")
	last_name = data.get("lastname")
	first_name = data.get("firstname")
	email = data.get("email")
	avatar = request.FILES.get("avatar")

	if not username:
		return JsonResponse(
			{"status": "error", "message": "Username is required."}, status=400
		)
	if not last_name:
		return JsonResponse(
			{"status": "error", "message": "Last name is required."}, status=400
		)
	if not first_name:
		return JsonResponse(
			{"status": "error", "message": "First name is required."}, status=400
		)
	if not email:
		return JsonResponse(
			{"status": "error", "message": "Email is required."}, status=400
		)

	if not re.match("^[a-zA-Z0-9_-]{3,20}$", username):
		return JsonResponse(
			{
				"status": "error",
				"message": "Invalid username. Use only alphanumeric characters, dashes and underscores. Length must be between 3 and 20 characters.",
			},
			status=400,
		)

	if not re.match("^[a-zA-Z0-9_-]{3,20}$", first_name):
		return JsonResponse(
			{
				"status": "error",
				"message": "Invalid first name. Use only alphanumeric characters, dashes and underscores. Length must be between 3 and 20 characters.",
			},
			status=400,
		)

	if not re.match("^[a-zA-Z0-9_-]{3,20}$", last_name):
		return JsonResponse(
			{
				"status": "error",
				"message": "Invalid last name. Use only alphanumeric characters, dashes and underscores. Length must be between 3 and 20 characters.",
			},
			status=400,
		)

	if not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
		return JsonResponse(
			{"status": "error", "message": "Invalid email address."}, status=400
		)

	try:
		CustomUser.objects.filter(username=request.user.username).update(
			username=username,
			first_name=first_name,
			last_name=last_name,
			email=email
		)
		if avatar:
			CustomUser.objects.filter(username=request.user.username).update(avatar=avatar)
	except CustomUser.DoesNotExist:
		return JsonResponse(
			{"status": "error", "message": "User not found."}, status=404
		)

	return JsonResponse(
		{"status": "ok", "message": "Your profile has been successfully updated!"}
	)


@require_http_methods(["POST"])
def change_password(request):
	data = request.POST
	try:
		user = CustomUser.objects.get(username=request.user.username)
	except CustomUser.DoesNotExist:
		return JsonResponse(
			{"status": "error", "message": "User not found."}, status=404
		)

	password = data.get("old_password")
	if not check_password(password, request.user.password):
		return JsonResponse(
			{"status": "error", "message": "Incorrect password."}, status=400
		)

	new_password = data.get("new_password")
	if not new_password:
		return JsonResponse(
			{"status": "error", "message": "New password is required."}, status=400
		)
	elif len(new_password) < 8:
		return JsonResponse(
			{
				"status": "error",
				"message": "Password must be at least 8 characters long.",
			},
			status=400,
		)

	confirm_password = data.get("confirm_password")
	if new_password != confirm_password:
		return JsonResponse(
			{"status": "error", "message": "Passwords do not match."}, status=400
		)

	user.set_password(new_password)
	user.save()
	return JsonResponse(
		{"status": "ok", "message": "Your password has been successfully updated!"},
		status=200,
	)
