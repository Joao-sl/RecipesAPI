from django.apps import AppConfig


class RecipesapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipesAPI'

    def ready(self) -> None:
        import recipesAPI.signals
        return super().ready()
