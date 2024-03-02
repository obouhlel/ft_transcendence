from typing import Any
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.db import models
from django.utils import timezone


# AbstractUser has the following fields:
# - username
# - first_name
# - last_name
# - email
# - password
# - groups
# - user_permissions
# - is_staff
# - is_active
# - is_superuser
# - last_login
# - date_joined
class CustomUser(AbstractUser):
	is_admin = models.BooleanField(default=False)
	sexe = models.CharField(max_length=64, default='Unknow')
	birthdate = models.DateField(default=timezone.now)
	token = models.CharField(max_length=128)
	avatar = models.ImageField(upload_to='avatars/')
	created_at = models.DateTimeField(default=timezone.now)
	last_connexion = models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length=30, default='Online')
	list_friends = models.ManyToManyField('self')
	def __str__(self):
		return self.username
	def update_status(self, status: str):
		self.status = status
		self.save()
	def update_last_connexion(self):
		self.last_connexion = timezone.now()
		self.save()
	def update_avatar(self, avatar: str):
		self.avatar = avatar
		self.save()
	def user_data(self):
		return {
			'id': self.id,
			'email': self.email,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'is_active': self.is_active,
			'is_superuser': self.is_superuser,
			'last_login': self.last_login,
			'date_joined': self.date_joined,
			'username': self.username,
			'is_admin': self.is_admin,
			'sexe': self.sexe,
			'birthdate': self.birthdate,
			'avatar': self.avatar.path if self.avatar else None,
			'created_at': self.created_at,
			'last_connexion': self.last_connexion,
			'status': self.status,
			'friends_received': self.getFriendRequestReceived(),
			'request_sent': self.getFriendRequestSent(),
			'list_friends': self.getFriends(),
			'stat': self.getStat()
		}
	def getFriends(self):
		list_friends = self.list_friends.all()
		return [friend.id for friend in list_friends]
	def getFriendRequestReceived(self):
		list_friend_request = self.receiver.all()
		return [re.friend_request_data() for re in list_friend_request]
	def getFriendRequestSent(self):
		list_friend_request = self.sender.all()
		return [re.friend_request_data() for re in list_friend_request]
	def getStat(self):
		list_stat = self.stat_user_by_game_set.all()
		return [stat.stat_user_by_game_data() for stat in list_stat]
	def get_notifications(self):
		list_notification = self.notification_set.all()
		notification = [notification.notification_data() for notification in list_notification]
		return notification


class FriendRequest(models.Model):
	id = models.AutoField(primary_key=True)
	sender = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='sender')
	receiver = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='receiver')
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.receiver.username + ' received a friend request from ' + self.sender.username
	def friend_request_data(self):
		return {
			'id': self.id,
			'id_sender': self.sender.username,
			'id_receiver': self.receiver.username,
			'created_at': self.created_at,
	}
