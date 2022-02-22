from django.apps import AppConfig


class TweetManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tweet_manager'

    def ready(self) -> None:
        
       
        from .tasks import handle_fetch_twitter_user_tweets_task
        from .tasks import analyse_celebrity_tweet_task
        handle_fetch_twitter_user_tweets_task.delay()
        analyse_celebrity_tweet_task.delay()

       

    
        return super().ready()