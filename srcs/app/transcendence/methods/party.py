
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from transcendence.models  import Party, Game, CustomUser, Stat_Game, Stat_User_by_Game
import json
from django.utils import timezone

#CRUD : Create, Read, Update, Delete
#Create: POST
#Read: GET
#Update: PUT
#Delete: DELETE


#---------------------------------GET PARTY---------------------------------#
@login_required
@require_http_methods(['GET'])
def getPartyById(request, id):
	try:
		party = Party.objects.get(id=id)
		data = party.party_data()
		return JsonResponse({'status': 'ok', 'party': data})
	except Party.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This party does not exist.'}, status=404)

@login_required
@require_http_methods(['GET'])
def getAllParties(request):
	parties = Party.objects.all()
	data = []
	for party in parties:
		data += [party.party_data()]
	return JsonResponse({'status': 'ok', 'parties': data})

@login_required
@require_http_methods(['GET'])
def getPartyByGame(request, id_game):
	try:
		game = Game.objects.get(id=id_game)
		parties = game.party_game.all()
		data = [party.party_data() for party in parties]
		return JsonResponse({'status': 'ok', 'parties': data})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
	except Party.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This party does not exist.'}, status=404)


@login_required
@require_http_methods(['GET'])
def getUserInParty(request, id_party):
	try:
		party = Party.objects.get(id=id_party)
		users = [party.player1, party.player2]
		data = [user.user_data() for user in users]
		return JsonResponse({'status': 'ok', 'party': data})
	except Party.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This party does not exist.'}, status=404)

@login_required
@require_http_methods(['GET'])
def getUserHistoryByGame(request, id_game):
    try:
        game = Game.objects.get(id=id_game)
        user = request.user
        parties = Party.objects.filter(game=game, player1=user) | Party.objects.filter(game=game, player2=user)
        data = [party.party_data() for party in parties]
        return JsonResponse({'status': 'ok', 'parties': data})
    except Game.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)


# -------------------------------POST PARTY-----------------------------#
@login_required
@require_http_methods(['POST'])
def createParty(request):
	data = json.loads(request.body)
	id_game = data['id_game']
	id_user1 = data['id_user1']
	id_user2 = data['id_user2']
	try:
		game = Game.objects.get(id=id_game)
		user1 = CustomUser.objects.get(id=id_user1)
		user2 = CustomUser.objects.get(id=id_user2)
		party = Party.objects.create(id_game=game, player1=user1, player2=user2,
							   started_at=timezone.now())
		return JsonResponse({'status': 'ok', 'message': 'Party created successfully.'})
	except Game.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This game does not exist.'}, status=404)
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)

@login_required
@require_http_methods(['POST'])
def addUserToParty(request, id_party):
	data = json.loads(request.body)
	id_party = data['id_party']
	id_user = data['id_user']
	try:
		party = Party.objects.get(id=id_party)
		user = CustomUser.objects.get(id=id_user)
		party.player2 = user
		party.save()
		return JsonResponse({'status': 'ok', 'message': 'User added successfully.'})
	except Party.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This party does not exist.'}, status=404)
	except CustomUser.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'This user does not exist.'}, status=404)


def isUserInParty(party, user):
	if party.player1 == user or party.player2 == user:
		return True
	else:
		return False
def EndPartyinTournament(tournament, party):
	#End party first
	party.update_end()


