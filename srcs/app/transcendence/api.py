from django.urls import path
from .methods import *

urlpatterns = [
	path('login/', login_user, name='login'),
	path('login42/', login_42, name='login42'),
	path('register/', register_user, name='register'),
	path('logout/', logout_user, name='logout'),
	path('edit_profile/', edit_profile, name='edit_profile'),
	path('get_all_users/', getAllUsers, name='getAllUsers'),
	path('get_user_by_id/<int:id>', getUserById, name='getUserById'),
	path('get_user_by_username/<str:username>', getUserByName, name='getUserByName'),
	path('get_user_name/', getUserName, name='getUserName'),
	path('get_game_by_id/<int:id>', getGameById, name='getGameById'),
	path('get_game_by_name/<str:name>', getGameByName, name='getGameByName'),
	path('get_all_games/', getAllGames, name='getAllGames'),

	path('get_user_in_lobby/<int:id_game>', getUsersInLobby, name='getUsersInLobby'),
	# path('get_user_in_lobby/<int:id_game>/<int:id_lobby>', get_user_in_lobby, name='get_user_in_lobby'),
	path('get_all_friends/<int:id_user>', getAllFriendsofUser, name='getAllFriends'),
	path('get_all_request/<int:id_user>', getAllFriendRequestofUser, name='getAllFriendRequestofUser'),
	path('get_stats_users_by_game/<int:id_game>', getStatsUsersByGame, name='getStatsUsersByGame'),
	path('add_win_to_user/<int:id_game>', addWinToUser, name='addWinToUser'),
	path('get_all_lobbies/', getAllLobbies, name='getAllLobbies'),
	path('get_lobby_by_id/<int:id>', getLobbyById, name='getLobbyById'),

	path('get_all_tournaments/', getAllTournaments, name='getAllTournaments'),
	path('get_tournament_by_id/<int:id>', getTournamentById, name='getTournamentById'),
	path('get_tournament_by_game/<int:id>', getTournamentByGame, name='getTournamentByGame'),


]
