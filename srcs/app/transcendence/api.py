from django.urls import path
from .methods import * 

urlpatterns = [
	path('login/', login_user, name='login'),
	path('register/', register_user, name='register'),
	path('logout/', logout_user, name='logout'),
	path('edit_profile/', edit_profile, name='edit_profile'),
	# path('profile/', methods.profile, name='profile'),
	# path('games/', methods.games, name='games'),
	# path('game/', methods.game, name='game'),
    # path('pong/', methods.pong, name='pong'),
	# path('shooter/', methods.shooter, name='shooter'),
	path('get_all_users/', getAllUsers, name='getAllUsers'),
	path('get_user_by_id/<int:id>', getUserById, name='getUserById'),
	path('get_user_by_username/<str:username>', getUserByName, name='getUserByName'),
	path('get_user_name/', getUserName, name='getUserName'),
	path('get_game_by_id/<int:id>', getGameById, name='getGameById'),
	path('get_game_by_name/<str:name>', getGameByName, name='getGameByName'),
	path('get_all_games/', getAllGames, name='getAllGames'),

	path('get_all_lobbies/', getAllLobbies, name='getAllLobbies'),
	path('get_lobby_by_id/<int:id>', getLobbyById, name='getLobbyById'),
	
	path('get_all_tournaments/', getAllTournaments, name='getAllTournaments'),
	path('get_tournament_by_id/<int:id>', getTournamentById, name='getTournamentById'),
	path('get_tournament_by_game/<int:id>', getTournamentByGame, name='getTournamentByGame'),
	
	

	
	
	
]
