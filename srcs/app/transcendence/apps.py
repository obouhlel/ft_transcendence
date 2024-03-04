from django.apps import AppConfig

class TranscendenceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transcendence'

    # 1. 👇 Add this line for signals
    def ready(self):
        import transcendence.signals
