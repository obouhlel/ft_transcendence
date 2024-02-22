from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Game, CustomUser

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
		statofgame = game.stat_game
		data = statofgame.Stat_game_data()
		return JsonResponse({'status': 'ok', 'stat': data})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)


# -------------------------------POST STAT-----------------------------#
#no need to create a stat for a user or a game, it is created automatically when a user or a game is created

# -------------------------------PUT STAT-----------------------------#
# when a party is finished, the stat of the user and the game are updated
#TODO
	
# -------------------------------DELETE STAT-----------------------------#
#not implemented