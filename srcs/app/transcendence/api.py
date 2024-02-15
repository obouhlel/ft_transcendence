from django.urls import path
from . import methods

urlpatterns = [
	path('login/', methods.login_user, name='login'),
	path('login42/', methods.login_42, name='login42'),
	path('register/', methods.register_user, name='register'),
    path('logout/', methods.logout_user, name='logout'),
	path('edit_profile/', methods.edit_profile, name='edit_profile'),
	path('profile/', methods.profile, name='profile'),
	path('games/', methods.games, name='games'),
	path('game/', methods.game, name='game'),
    path('pong/', methods.pong, name='pong'),
	path('shooter/', methods.shooter, name='shooter'),
]