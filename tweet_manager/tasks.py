import imp
from time import sleep
from celery import shared_task

# local import
from .tweet_api import get_date


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

        
        
    



# done: create the task for that divides the analysed tweets 
# into 10 groups that is arranged according to tweet_id
# for each celebrity twitter user
@shared_task(bind=True)
def generate_time_series_summary(self):
    # local import
    from UserManager.models import TwitterUser
    from .models import TimeSeriesSummary,Tweet
    # getting all the analysing and non protected users 
    while True:
        analysing_user = TwitterUser.objects.filter(isAnalysing=True,protected=False)

        # for each analysing user
        for user in analysing_user:
            # gettting all the analysed tweets of the given user according to ascending order o tweet_id

            all_analysed_tweets = Tweet.objects.filter(is_analysed=True,twitter_user = user).order_by('tweet_id')
            
            # creating TimeSeriesSummary only if analysed_tweets length is greater than 10
            n_all_analysed_tweets = len(all_analysed_tweets)
            if n_all_analysed_tweets > 10:
                # calculating the partition indices
                partition = [0]
                for i in range(1,11):
                    pos = round(n_all_analysed_tweets/10 * i)

                    partition.append(int(pos))
                
                # partitioning the tweets 
                # [[partion0],[partion1],....,[partition9]]
                # print(type(all_analysed_tweets)) <class QuerySet>
                partitioned_tweets = []
                for i in range(10):
                    single_partition = all_analysed_tweets[partition[i]:partition[i+1]+1]
                    # print(type(single_partition))  <class 'list'>
                    partitioned_tweets.append(single_partition)


                for position,tweets in enumerate(partitioned_tweets):

                    # calculating first number of  positive and negative tweets 
                    n_total_tweets = len(tweets)
                    # n_positive = len(tweets.filter(label="POSITIVE")) # ERROR: 
                    # https://stackoverflow.com/questions/37192617/filtering-a-django-queryset-once-a-slice-has-been-taken?rq=1

                    # counting positive tweets 
                    n_positive = 0
                    for tweet in tweets:
                        if tweet.label == "POSITIVE":
                            n_positive += 1
                    
                    n_negative = n_total_tweets - n_positive

                    # print(n_positive,n_negative,n_total_tweets)

                    # getting  or creating TimeSeriesSummary 
                    last_tweet = tweets[-1]
                    last_tweet_date=get_date(last_tweet.tweet_id)
                    current_pos_current_user_time_series_summary,_ = TimeSeriesSummary.objects.get_or_create(twitter_user = user,position = position)
                    
                    current_pos_current_user_time_series_summary.positive = n_positive
                    current_pos_current_user_time_series_summary.negative = n_negative
                    current_pos_current_user_time_series_summary.total = n_total_tweets
                    current_pos_current_user_time_series_summary.date = last_tweet_date
                    current_pos_current_user_time_series_summary.save()
                print(f"generate_time_series_summary---{user}")
        sleep(10)

# TODO: send signal of the that users only that have completed upto grouping 
