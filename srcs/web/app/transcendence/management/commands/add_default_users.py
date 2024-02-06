from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from transcendence.models import User  # Remplacez 'your_app_name' par le nom de votre application

class Command(BaseCommand):
    help = 'Add default users to the database'

    def handle(self, *args, **options):
        # Créer les utilisateurs
        user1 = User.objects.create(
            username='admin',
            email='admin@admin.fr',
            password=make_password('adminadmin'),
            firstname='admin',
            lastname='admin',
            sexe='Male',
            birthdate=timezone.now() - timezone.timedelta(days=25*365),  # Remplacez par la date de naissance réelle
            date_creation=timezone.now(),
            date_last_connection=timezone.now(),
            id_list_friend=None
        )

        user2 = User.objects.create(
            username='user2',
            email='user2@email.com',
            password=make_password('password2'),
            firstname='User',
            lastname='Two',
            sexe='Female',
            birthdate=timezone.now() - timezone.timedelta(days=30*365),  # Remplacez par la date de naissance réelle
            date_creation=timezone.now(),
            date_last_connection=timezone.now(),
            id_list_friend=None
        )
