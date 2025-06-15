# from django.apps import AppConfig


# class UserauthsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'userauths'

# userauths/apps.py
# userauths/apps.py
from django.apps import AppConfig


class UserauthsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userauths'

    def ready(self):
        # IMPORTANT: Import your models file here because your signals are defined within it.
        import userauths.models