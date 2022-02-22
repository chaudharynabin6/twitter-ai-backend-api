import imp
from time import sleep
from celery import shared_task

# local import



@shared_task(bind=True)
def handle_fetch_twitter_user_tweets_task(self):
    # local import
    from UserManager.models import TwitterUser
    from .controller.fetch_tweets import fetch_tweets_and_save_to_db


    while True:
        analysable_users = TwitterUser.objects.filter(isAnalysing=True,protected=False)
        for item in analysable_users:
            fetch_tweets_and_save_to_db(id=item.user_id)
        
        sleep(20)

    return 'Task Completed'


@shared_task(bind=True)
def analyse_celebrity_tweet_task(self):
    from transformers import pipeline
    from .models import Tweet
    pipe = pipeline("text-classification")    
    non_anlysed_tweets = Tweet.objects.filter(is_analysed=False)

    for tweet in non_anlysed_tweets:
        text = tweet.text
        output = pipe(text)[0]
        label = output.get("label")
        score = output.get('score')
        tweet.label = label
        tweet.score = score
        tweet.is_analysed = True
        tweet.save()
        print(f"{tweet.tweet_id} analysed")


# TODO: create the task for calculating the total of
#  postive and negative and total analysed tweets 
# for each celebrity

# TODO: create the task for that divides the analysed tweets 
# into 10 groups according to arranged according to tweet_id
# for each celebrity

# TODO: send signal of the that users only that have completed upto grouping 
