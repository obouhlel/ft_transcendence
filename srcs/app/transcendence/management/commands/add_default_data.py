from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from transcendence.models import CustomUser, Game, Stat_Game, Lobby

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

		user2 = CustomUser.objects.create(
			username='user2',
			email='user2@email.com',
			password=make_password('password2'),
			first_name='User',
			last_name='Two',
			sexe='F',
			birthdate=timezone.now() - timezone.timedelta(days=30*365), 	
		)

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
			genre='Arcade, Sports, Action, Classic, Paddle, Simulation (Simple), Retro',
			stat=stat_game1
		)
		game1.save()

		stat_game2 = Stat_Game()
		stat_game2.save()

		game2 = Game.objects.create(
			name='Tictactoe',
			description='description2',
			genres='genre2',
			stat=stat_game2
		)
		game2.save()

		# lobby = Lobby.objects.create(type='Public',id_game=game1)
		# lobby.user.add(user1)
		# lobby.user.add(user2)
		# game1.lobby_game.add(lobby)
		# lobby.save()