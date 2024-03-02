from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from transcendence.models import Party , CustomUser, Game, Stat_Game, Lobby, Stat_User_by_Game

class Command(BaseCommand):
	help = 'Add default users to the database'

	def handle(self, *args, **options):
		user1 = CustomUser.objects.create(
			username='admin',
			email='admin@admin.fr',
			password=make_password('adminadmin'),
			first_name='admin',
			last_name='admin',
			sexe='M',
			birthdate=timezone.now() - timezone.timedelta(days=25*365),
			is_superuser=True,
			is_staff=True
		)
		user1.save()

		user2 = CustomUser.objects.create(
			username='user2',
			email='user2@email.com',
			password=make_password('password2'),
			first_name='User',
			last_name='Two',
			sexe='F',
			birthdate=timezone.now() - timezone.timedelta(days=30*365),
		)
		user2.save()

		stat_game1 = Stat_Game()
		stat_game1.save()

		description_pong = """
		Pong is a classic arcade game where players control paddles to hit a ball back and forth.\n
		Test your reflexes in this timeless battle of speed and skill.
		"""

		game1 = Game.objects.create(
			name='Pong',
			image='img/pong.jpg',
			description=description_pong,
			genres='Arcade, Sports, Action, Classic, Paddle, Simulation (Simple), Retro',
			stat=stat_game1
		)
		game1.save()

		stat_game2 = Stat_Game()
		stat_game2.save()

		game2 = Game.objects.create(name='shooter',description='description2',genre='genre2',stat=stat_game2)

		Stat_User_by_Game.objects.create(user=user1, game=game1)
		Stat_User_by_Game.objects.create(user=user2, game=game1)
		Stat_User_by_Game.objects.create(user=user1, game=game2)
		Stat_User_by_Game.objects.create(user=user2, game=game2)

		# Créer des parties
		party1 = Party.objects.create(
			game=game1,
			name='Party 1',
			started_at=timezone.now(),
			ended_at=timezone.now() + timezone.timedelta(minutes=10),
			status='Finished',
			player1=user1,
			player2=user2,
			score1=10,
			score2=5,
			winner_party=user1,
			loser_party=user2
		)

		party2 = Party.objects.create(
			game=game2,
			name='Party 2',
			started_at=timezone.now(),
			ended_at=timezone.now() + timezone.timedelta(minutes=15),
			status='Finished',
			player1=user1,
			player2=user2,
			score1=7,
			score2=10,
			winner_party=user2,
			loser_party=user1
		)

		party3 = Party.objects.create(
			game=game1,
			name='Party 3',
			started_at=timezone.now(),
			ended_at=timezone.now() + timezone.timedelta(minutes=20),
			status='Finished',
			player1=user1,
			player2=user2,
			score1=3,
			score2=10,
			winner_party=user2,
			loser_party=user1
		)
		# Ajouter les parties aux statistiques des utilisateurs
		user1_stat_game1 = Stat_User_by_Game.objects.get(user=user1, game=game1)
		user1_stat_game1.nb_played += 1
		user1_stat_game1.nb_win += 1
		user1_stat_game1.save()

		user2_stat_game1 = Stat_User_by_Game.objects.get(user=user2, game=game1)
		user2_stat_game1.nb_played += 1
		user2_stat_game1.nb_lose += 1
		user2_stat_game1.save()

		user1_stat_game1.nb_played += 1
		user1_stat_game1.nb_lose += 1
		user1_stat_game1.save()

		user2_stat_game1.nb_played += 1
		user2_stat_game1.nb_win += 1
		user2_stat_game1.save()

		user1_stat_game2 = Stat_User_by_Game.objects.get(user=user1, game=game2)
		user1_stat_game2.nb_played += 1
		user1_stat_game2.nb_lose += 1
		user1_stat_game2.save()

		user2_stat_game2 = Stat_User_by_Game.objects.get(user=user2, game=game2)
		user2_stat_game2.nb_played += 1
		user2_stat_game2.nb_win += 1
		user2_stat_game2.save()

		description_tictactoe = """
		Tic Tac Toe, also known as Naughts and Crosses, is a classic two-player game. 
		Players take turns marking spaces in a 3x3 grid, aiming to form a row, column, or diagonal of their symbol (X or O). 
		Simple yet strategic, it's a timeless test of wit and tactics.
		"""

		game2 = Game.objects.create(
			name='Tictactoe',
			description=description_tictactoe,
			genres='Puzzle, Board Game, Strategy',
			stat=stat_game2
		)
		game2.save()

		# lobby = Lobby.objects.create(type='Public',id_game=game1)
		# lobby.user.add(user1)
		# lobby.user.add(user2)
		# game1.lobby_game.add(lobby)
		# lobby.save()
