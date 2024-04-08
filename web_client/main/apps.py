from django.apps import AppConfig


class MainConfig(AppConfig):
    # Все модели в приложении main будут использовать BigAutoField для автоматически создаваемых первичных ключей.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
