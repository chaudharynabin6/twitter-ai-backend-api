from django.apps import AppConfig


class TweetManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tweet_manager'

    def ready(self) -> None:
        
       
        from .tasks import handle_fetch_twitter_user_tweets_task
        from .tasks import analyse_celebrity_tweet_task
        from .tasks import generate_total_summary
        # handle_fetch_twitter_user_tweets_task.delay()
        # analyse_celebrity_tweet_task.delay()
        generate_total_summary.delay()

       

    
        return super().ready()