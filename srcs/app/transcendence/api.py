from django.urls import path
from .methods import *
from .models import *

urlpatterns = [
    # FORMS
	path('login/', login_user, name='login'),
	path('login_42/', login_42, name='login42'),
    path('register_42/', register_42, name='register42'),
	path('logout/', logout_user, name='logout'),
	path('register/', register_user, name='register'),
	path('edit_profile/', edit_profile, name='edit_profile'),
    path('change_password/', change_password, name='change_password'),

	# GETERS
    # USERS
	path('get_all_users/', getAllUsers, name='getAllUsers'),
	path('get_user_by_id/<int:id>', getUserById, name='getUserById'),
	path('get_user_by_username/<str:username>', getUserByName, name='getUserByName'),
	path('get_user_name/', getUserName, name='getUserName'),
	path('me', getMe, name='getMe'),
	path('get_user_connected/', getUserConnected, name='getUserConnected'),
	path('get_all_friends/<int:id_user>', getAllFriendsofUser, name='getAllFriendsofUser'),

	#Leaderboard
	path('get_leaderboard/<int:id_game>', getLeaderboard, name='getLeaderboard'),
	path('get_leaderboard/<int:id_game>/<int:length>', getLeaderboard_length, name='getLeader'),

	# GAMES
	path('get_game_by_id/<int:id>', getGameById, name='getGameById'),
	path('get_game_by_name/<str:name>', getGameByName, name='getGameByName'),
	path('get_all_games/', getAllGames, name='getAllGames'),
	path('get_stats_by_game/<int:id_game>', getStatByGame, name='getStatByGame'),
	path('get_stats_users_by_game/<int:id_game>', getStatsUsersByGame, name='getStatsUsersByGame'),
	path('add_win_to_user/<int:id_game>', addWinToUser, name='addWinToUser'), # a supprimer

	path('get_user_history_by_game/<int:id_game>', getUserHistoryByGame, name='getUserHistoryByGame'),
	path('get_all_party/', getAllParties, name='getPartyById'),

	path('get_all_lobbies/', getAllLobbies, name='getAllLobbies'),
	path('get_lobby_by_id/<int:id>', getLobbyById, name='getLobbyById'),
	path('get_all_party/', getAllParties, name='getPartyById'),

	# path('join_lobby/', joinLobby, name='joinLobby'),
	path('quit_lobby/', quitLobby, name='quitLobby'),

	# path('add_win_to_user/<int:id_game>', addWinToUser, name='addWinToUser'),
	# TOURNAMENTS
	path('get_all_tournaments/', getAllTournaments, name='getAllTournaments'),
	path('get_tournament_by_id/<int:id>', getTournamentById, name='getTournamentById'),
	path('get_tournament_by_game/<int:id>', getTournamentByGame, name='getTournamentByGame'),
    path('alias/', postAlias, name='alias'),
	path('search_user/<str:username>', searchUser, name='searchUser'),

	path('join_tournament/', joinTournament, name='joinTournament'),
	path('create_tournament/', createTournament, name='createTournament'),
	path('leave_tournament/', leaveTournament, name='quitTournament'),

	path('get_all_friends/<int:id_user>', getAllFriendsofUser, name='getAllFriendsofUser'),
	path('add_friend/', sendFriendRequest, name='addFriend'),
	path('delete_friend/<int:id_user>', deleteFriend, name='deleteFriend'),
	path('respond_friend_request/', RespondFriendRequest, name='acceptFriendRequest'),
	path('get_friend_request/', getFriendRequest, name='getFriendRequest'),
	path('accept_friend_request/<int:id_user>', acceptFriendRequest, name='acceptFriendRequest'),
]
