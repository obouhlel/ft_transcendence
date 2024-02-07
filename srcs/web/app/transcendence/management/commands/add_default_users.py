from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from transcendence.models import CustomUser  # Remplacez 'transcendence' par le nom de votre application


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
            birthday=timezone.now() - timezone.timedelta(days=25*365),  # Remplacez par la date de naissance réelle
        )

        user2 = CustomUser.objects.create(
            username='user2',
            email='user2@email.com',
            password=make_password('password2'),
            first_name='User',
            last_name='Two',
            sex='F',
            birthday=timezone.now() - timezone.timedelta(days=30*365),  # Remplacez par la date de naissance réelle
            date_joined=timezone.now(),
            last_login=timezone.now(),
        )
