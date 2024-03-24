from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from transcendence.models import Party , CustomUser, Game, Stat_Game, Lobby, Stat_User_by_Game

class Command(BaseCommand):
	help = 'Add default users to the database'

	def handle(self, *args, **options):
		# Créer des utilisateurs

		

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
		In tournament mode, it's a draw, the first player loses.
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

	#add some details to superuser
		superusers = CustomUser.objects.filter(is_superuser=True)
		if superusers:
			i = 0
			for user in superusers:
				user.first_name = 'Admin' + str(i)
				user.last_name = 'Transcendence'
				user.sexe = 'O'
				user.birth_date = "1990-01-01"
				user.save()
				for game in Game.objects.all():
					stat_user_by_game, _created = Stat_User_by_Game.objects.get_or_create(user=user, game=game)
					stat_user_by_game.save()
				