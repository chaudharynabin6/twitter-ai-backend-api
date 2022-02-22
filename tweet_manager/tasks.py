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


# done: create the task for calculating the total of
#  postive and negative and total analysed tweets 
# for each celebrity

@shared_task(bind=True)
def generate_total_summary(self):
    # local import
    from UserManager.models import TwitterUser
    from .models import TotalSummary,Tweet
    # getting all the analysing and non protected users 
    while True:
        analysing_user = TwitterUser.objects.filter(isAnalysing=True,protected=False)

        # for each analysing user
        for user in analysing_user:
            # gettting all the analysed tweets of the given user

            all_analysed_tweets = Tweet.objects.filter(is_analysed=True,twitter_user = user)

            # fitering only the positive tweets
            positive_tweets = all_analysed_tweets.filter(label="POSITIVE")

            n_all_analysed_tweets = len(all_analysed_tweets)
            n_positive_tweets = len(positive_tweets)

            n_negative_tweets = n_all_analysed_tweets - n_positive_tweets
        

            total_summary,_=TotalSummary.objects.get_or_create(twitter_user=user)

            total_summary.positive = n_positive_tweets
            total_summary.negative = n_negative_tweets
            total_summary.total = n_all_analysed_tweets
            total_summary.save()
            print(f"Total Summary of {user}")
        sleep(20)

        
        
    



# TODO: create the task for that divides the analysed tweets 
# into 10 groups that is arranged according to tweet_id
# for each celebrity twitter user



# TODO: send signal of the that users only that have completed upto grouping 
