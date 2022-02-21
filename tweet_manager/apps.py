from django.apps import AppConfig


class TweetManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tweet_manager'

    def ready(self) -> None:
        # from .controller.main import main
        from .controller.fetch_tweets import fetch_tweets_and_save_to_db
        from .tasks import test_funcion
        test_funcion.delay()
        # fetch_tweets_and_save_to_db('180505807')

        # main()
        return super().ready()