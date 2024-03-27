from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_http_methods
from transcendence.models import CustomUser
import re
import logging
from django.db import models
from PIL import Image

logger = logging.getLogger(__name__)

def error_response(message):
	return JsonResponse({"status": "error", "message": message + " is required."}, status=400)

@require_http_methods(["POST"])
def edit_profile(request):
	data = request.POST
	username = data.get("username")
	last_name = data.get("lastname")
	first_name = data.get("firstname")
	email = data.get("email")
	password = data.get("password")
	data_list = [username, password, email, first_name, last_name]
	avatar = None
	if len (request.FILES) > 0:
		avatar = request.FILES["avatar"]

	if not password:
		return error_response("Password")
	
	if not check_password(password, request.user.password):
		return JsonResponse(
			{"status": "error", "message": "Incorrect password."}, status=400
		)

	if not username:
		return error_response("Username")
	
	if not last_name:
		return error_response("Last name")
	if not first_name:
		return error_response("First name")
	
	if not email:
		return error_response("Email")

	for d in data_list:
		if len(d) > 50:
			return JsonResponse({'status': 'error', 'message': 'Data is too long.'}, status=400)
		
	if not re.match("^[a-zA-Z0-9_-]{3,20}$", username):
		return JsonResponse(
			{
				"status": "error",
				"message": "Invalid username. Use only alphanumeric characters, dashes and underscores. Length must be between 3 and 20 characters.",
			},
			status=400,
		)

	if not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
		return JsonResponse(
			{"status": "error", "message": "Invalid email address."}, status=400
		)

	try:
		user = CustomUser.objects.get(username=request.user.username)
		if username:
			#check if the username is already taken	
			if CustomUser.objects.filter(username=username).exclude(id=user.id).exists():
				return JsonResponse(
					{"status": "error", "message": "Username already taken."}, status=400
				)
			user.username = username
		if email:
			#check if the email is already taken
			if CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
				return JsonResponse(
					{"status": "error", "message": "Email already taken."}, status=400
				)
			user.email = email
		if first_name:
			user.first_name = first_name
		if last_name:
			user.last_name = last_name
		
		if avatar:
			#check if the image is valid
			try:
				img = Image.open(avatar)
				img.verify()
			except Exception as e:
				return JsonResponse(
					{"status": "error", "message": "Invalid image."}, status=400
				)

			#check the image size
			if avatar.size > 2 * 1024 * 1024:
				return JsonResponse(
					{"status": "error", "message": "Image size is too large."}, status=400
				)

			#delete the previous image
			old_avatar = user.avatar
			if old_avatar and old_avatar.name != 'avatars/default_avatar.png':
				old_avatar.delete(save=False)
			#save the new image
			user.avatar =  avatar
		user.save()

			
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
	new_password = data.get("new_password")
	confirm_password = data.get("confirm_password")

	if not password or not new_password or not confirm_password:
		return JsonResponse(
			{"status": "error", "message": "All fields are required."}, status=400
		)

	if not check_password(password, request.user.password):
		return JsonResponse(
			{"status": "error", "message": "Incorrect password."}, status=400
		)

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
