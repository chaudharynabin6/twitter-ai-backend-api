from django.apps import AppConfig


class TweetManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tweet_manager'

    def ready(self) -> None:
        # from .controller.main import main
        # main()
        return super().ready()