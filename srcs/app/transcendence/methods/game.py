
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from transcendence.models  import Game

#CRUD : Create, Read, Update, Delete
#Create: POST : Create a new game
#Read: GET : Get a game information by id or by name
#Update: PUT : Update a game information
#Delete: DELETE : Delete a game

# -------------------------------GET GAME-----------------------------#
@login_required
@require_http_methods(['GET'])
def getGameByName(request, name):
	try:
		game = Game.objects.get(name=name)
		data = game.game_data()
		return JsonResponse({'status': 'ok', 'game': data})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
	
@login_required
@require_http_methods(['GET'])
def getGameById(request, id):
	try:
		game = Game.objects.get(id=id)
		data = game.game_data()
		return JsonResponse({'status': 'ok', 'game': data})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
	
@login_required
@require_http_methods(['GET'])
def getAllGames(request):
	games = Game.objects.all()
	data = []
	for game in games:
		data += [game.game_data()]
	return JsonResponse({'status': 'ok', 'games': data})

# -------------------------------POST GAME-----------------------------#
#not implemented yet

# -------------------------------PUT GAME-----------------------------#
#not implemented yet

# -------------------------------DELETE GAME-----------------------------#
#not implemented yet