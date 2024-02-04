from django.db import models

# Create your models here.
class User(models.Model):
	id = models.AutoField(primary_key=True)
	login = models.CharField(max_length=30, unique=True)
	email = models.EmailField(max_length=254, unique=True)
	password = models.CharField(max_length=128)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)	
	is_admin = models.BooleanField(default=False)
	sex = models.CharField(max_length=1, default='N')
	age = models.IntegerField(default=0)
	token = models.CharField(max_length=128, unique=True)
	avatar = models.CharField(max_length=128, default='/var/www/static/default_avatar.png')
	created_at = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.login
