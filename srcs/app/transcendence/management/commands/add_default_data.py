from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from transcendence.models import CustomUser  # Remplacez 'transcendence' par le nom de votre application
from transcendence.models import Game  # Remplacez 'transcendence' par le nom de votre application
from transcendence.models import Stat_Game, Lobby  # Remplacez 'transcendence' par le nom de votre application

class Command(BaseCommand):
	help = 'Add default users to the database'

	def handle(self, *args, **options):
		# Créer les utilisateurs
		user1 = CustomUser.objects.create(
			username='admin',
			email='admin@admin.fr',
			password=make_password('adminadmin'),
			first_name='admin',
			last_name='admin',
			sexe='M',
			birthdate=timezone.now() - timezone.timedelta(days=25*365),  # Remplacez par la date de naissance réelle
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
			birthdate=timezone.now() - timezone.timedelta(days=30*365),  # Remplacez par la date de naissance réelle
		)

		stat_game1 = Stat_Game()
		stat_game1.save()
		game1 = Game.objects.create(
			name='pong',
			description='description1',
			genre='genre1',
			stat=stat_game1
		)

		lobby = Lobby.objects.create(type='Public',game=game1)
		# lobby.user.add(user1)
		# lobby.user.add(user2)
		# game1.lobby_game.add(lobby)
		# lobby.save()

		stat_game2 = Stat_Game()
		stat_game2.save()

		game2 = Game.objects.create(name='shooter',description='description2',genre='genre2',stat=stat_game2)
