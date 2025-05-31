from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # Importar señales aquí para que se registren correctamente
        import accounts.models # O específicamente 'import accounts.signals' si los separas
