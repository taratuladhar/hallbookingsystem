from django.apps import AppConfig


class HallConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hall'
    
    def ready(self):
        import hall.signals  # Import your signals module
