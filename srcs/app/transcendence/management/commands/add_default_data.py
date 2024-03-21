from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from transcendence.models import Party , CustomUser, Game, Stat_Game, Lobby, Stat_User_by_Game

class Command(BaseCommand):
	help = 'Add default users to the database'

	def handle(self, *args, **options):
		# Créer des utilisateurs

		user1 , _created = CustomUser.objects.get_or_create(
			username='admin',
			email='admin@admin.fr',
			password='pbkdf2_sha256$720000$mZq8LupVHlUqJko8DreAal$CW0qJRNmGjsI+R1ERf95FXWPSkcZlXvRMgr4mAQGQbI=', # adminadmin
			first_name='admin',
			last_name='admin',
			sexe='M',
			birthdate="1990-01-01",
			is_superuser=True,
			is_staff=True
		)
		user1.save()

		user2 , _created = CustomUser.objects.get_or_create(
			username='user2',
			email='user2@email.com',
			password='pbkdf2_sha256$720000$mZq8LupVHlUqJko8DreAal$CW0qJRNmGjsI+R1ERf95FXWPSkcZlXvRMgr4mAQGQbI=', # adminadmin
			first_name='User',
			last_name='Two',
			sexe='F',
			birthdate="1990-01-01",
			is_superuser=False,
			is_staff=False
		)
		user2.save()

		user3 , _created = CustomUser.objects.get_or_create(
			username='user3',
			email='user3@email.com',
			password='pbkdf2_sha256$720000$mZq8LupVHlUqJko8DreAal$CW0qJRNmGjsI+R1ERf95FXWPSkcZlXvRMgr4mAQGQbI=', # adminadmin
			first_name='User',
			last_name='Two',
			sexe='F',
			birthdate="1990-01-01",
			is_superuser=False,
			is_staff=False
		)

		description_pong = """
		Pong is a classic arcade game where players control paddles to hit a ball back and forth.\n
		Test your reflexes in this timeless battle of speed and skill.
		"""
		rule_pong = """
		The game is played with two paddles and a ball. 
		The player controls the paddle on the left side of the screen, 
		while the opponent controls the paddle on the right side. 
		The goal is to hit the ball back and forth, 
		and the first player to miss a return loses the game.
		"""
		game1, _created = Game.objects.get_or_create(
			name='Pong',
			image='img/pong.jpg',
			description=description_pong,
			genre='Arcade, Sports, Action, Classic, Paddle, Simulation (Simple), Retro',
			rules=rule_pong,
		)

		Stat_Game.objects.get_or_create(game=game1)
		Lobby.objects.get_or_create(game=game1)


		description_tictactoe = """
		Tic Tac Toe, also known as Naughts and Crosses, is a classic two-player game.
		Players take turns marking spaces in a 3x3 grid, aiming to form a row, column, or diagonal of their symbol (X or O).
		Simple yet strategic, it's a timeless test of wit and tactics.
		"""
		rule_tictactoe = """
		The game is played on a 3x3 grid.
		Players take turns marking an empty cell with their symbol (X or O).
		The first player to form a row, column, or diagonal of their symbol wins the game.
		"""

		game2, _created = Game.objects.get_or_create(
			name='Tictactoe',
			image='img/tictactoe1.webp',
			description=description_tictactoe,
			genre='Puzzle, Board Game, Strategy',
			rules=rule_tictactoe,
		)

		Stat_Game.objects.get_or_create(game=game2)
		Lobby.objects.get_or_create(game=game2)


		user1_stat_game1, _created =Stat_User_by_Game.objects.get_or_create(user=user1, game=game1)
		user2_stat_game1, _created = Stat_User_by_Game.objects.get_or_create(user=user2, game=game1)
		user1_stat_game2, _created = Stat_User_by_Game.objects.get_or_create(user=user1, game=game2)
		user2_stat_game2, _created = Stat_User_by_Game.objects.get_or_create(user=user2, game=game2)
		user3_stat_game2, _created = Stat_User_by_Game.objects.get_or_create(user=user3, game=game1)
		user3_stat_game2, _created = Stat_User_by_Game.objects.get_or_create(user=user3, game=game2)

		# Créer des parties
		party1, _created = Party.objects.get_or_create(
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

		party2, _created = Party.objects.get_or_create(
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

		party3, _created = Party.objects.get_or_create(
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

		user1_stat_game1.nb_played += 1
		user1_stat_game1.nb_win += 1
		user1_stat_game1.save()

		
		user2_stat_game1.nb_played += 1
		user2_stat_game1.nb_lose += 1
		user2_stat_game1.save()

		user1_stat_game1.nb_played += 1
		user1_stat_game1.nb_lose += 1
		user1_stat_game1.save()

		user2_stat_game1.nb_played += 1
		user2_stat_game1.nb_win += 1
		user2_stat_game1.save()

		
		user1_stat_game2.nb_played += 1
		user1_stat_game2.nb_lose += 1
		user1_stat_game2.save()

		
		user2_stat_game2.nb_played += 1
		user2_stat_game2.nb_win += 1
		user2_stat_game2.save()
