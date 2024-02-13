# Lives in /my_app/manangement/commands/watch_files.py
import time

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from watchfiles import watch


class Command(BaseCommand):
    help = "Automatically calls collectstatic when the staticfiles get modified."

    def handle(self, *args, **options):
        print('WATCH_STATIC: Static file watchdog started.')
        #for changes in watch([str(x) for x in settings.STATICFILES_DIRS]):

        for changes in watch('./'):
            print(f'WATCH_STATIC: {changes}', end='')
            call_command("collectstatic", interactive=False)
