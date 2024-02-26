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

	path('get_all_games/', methods.get_all_games, name='get_all_games'),
	path('get_game_by_name/<str:name>', methods.get_game_by_name, name='get_all_games'),
	path('get_game_by_id/<int:id>', methods.get_game_by_id, name='get_all_games'),
	path('get_all_users/', methods.get_all_users, name='get_all_users'),
	path('get_user_by_id/<int:id>', methods.get_user_by_id, name='get_user_by_id'),
	path('get_user_by_username/<str:username>', methods.get_user_by_username, name='get_user_by_username'),
	path('get_user_in_lobby/<int:id_game>', methods.get_all_user_in_all_lobby, name='get_user_in_lobby'),
	path('get_user_in_lobby/<int:id_game>/<int:id_lobby>', methods.get_user_in_lobby, name='get_user_in_lobby'),
	path('get_all_friends/', methods.get_all_friends, name='get_all_friends'),
	path('get_all_blocked/', methods.get_all_blocked, name='get_all_blocked'),
	path('get_all_request/', methods.get_all_request, name='get_all_request'),
	path('get_stats_users_by_game/<int:id_game>', methods.get_stats_users_by_game, name='get_stats_users_by_game'),
	path('add_win_to_user/<int:id_game>', methods.add_win_to_user, name='add_win_to_user'),
]
