from django.apps import AppConfig


class VidConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vid'

    def ready(self):
        # from .signals import start_transcoding
        from .signals import start_transcoding
