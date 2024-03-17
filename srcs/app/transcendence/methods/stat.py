from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from transcendence.models  import Game, CustomUser, Stat_User_by_Game

#CRUD : Create, Read, Update, Delete
#Create: POST : Create stat for a user or a game for the first time
#Read: GET : Get stat for a user or a game
#Update: PUT : Update stat for a user or a game
#Delete: DELETE : Delete stat for a user or a game


#---------------------------------GET STAT---------------------------------#
@login_required
@require_http_methods(['GET'])
def getStatByUser(request, id_user):
	try:
		user = CustomUser.objects.get(id=id_user)
		statofuser = user.stat
		data = statofuser.stat_user_by_game_data()
		return JsonResponse({'status': 'ok', 'stat': data})
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)

@login_required
@require_http_methods(['GET'])
def getStatByGame(request, id_game):
	try:
		game = Game.objects.get(id=id_game)
		statofgame = game.stat
		data = statofgame.stat_game_data()
		return JsonResponse({'status': 'ok', 'stat': data})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)

@login_required
@require_http_methods(['GET'])
def getStatsUsersByGame(request, id_game):
	try:
		game = Game.objects.get(id=id_game)
		try:
			stat_user = request.user.stats.get(game=game)
			data = {
				'nb_played': stat_user.nb_played,
				'time_played': stat_user.time_played,
				'nb_win': stat_user.nb_win,
				'nb_lose': stat_user.nb_lose,
			}
			return JsonResponse({'status': 'ok', 'stat': data})
		except Stat_User_by_Game.DoesNotExist:
			return JsonResponse({'status': 'error', 'message': 'No game stats for this user.'}, status=404)
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game doesn\'t exist.'}, status=404)


# -------------------------------POST STAT-----------------------------#
#no need to create a stat for a user or a game, it is created automatically when a user or a game is created
def addWinToUser(request, id_game):
	if request.method == 'POST':
		if request.user.is_authenticated:
			try:
				game = Game.objects.get(id=id_game)
				stat_user = request.user.stats.get(id_game=game)
				stat_user.nb_win += 1
				stat_user.save()
				return JsonResponse({'status': 'ok', 'message': 'Statistiques mises à jour avec succès.'})
			except Game.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'This game doesn\'t exist.'}, status=404)
		else:
			return JsonResponse({'status': 'error', 'message': 'Not authentificated.'}, status=401)
	else:
		return JsonResponse({'status': 'error', 'message': 'invalide methode.'}, status=405)
# -------------------------------PUT STAT-----------------------------#
# when a party is finished, the stat of the user and the game are updated
#TODO

# -------------------------------DELETE STAT-----------------------------#
#not implemented
