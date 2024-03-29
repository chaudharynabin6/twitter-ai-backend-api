from time import sleep
from typing import Dict, List
from django.core.exceptions import ObjectDoesNotExist
from requests.exceptions import ConnectionError
import pprint

# local package
from .tweepy_api import TweetAPI
from tweet_manager.serializers import TweetSerializer,TwitterUserMetaDataSerializer
from tweet_manager.models import TwitterUserMetaData,Tweet

from UserManager.models import TwitterUser

def save_tweets(id,data):
    # pprint.pprint(data)
    meta : Dict = data.get('meta')
    print("-------------------------------meta start---------------------")
    pprint.pprint(meta)
    print("-------------------------------meta end--------------------")
    result_count : int = meta.get('result_count',None)
    if result_count != 0 and result_count != None:
        twitter_user = TwitterUser.objects.get(user_id = id)
        twitter_user_meta_data,created = TwitterUserMetaData.objects.get_or_create(twitter_user = twitter_user)
        twitter_user_meta_data_serializer = TwitterUserMetaDataSerializer(instance=twitter_user_meta_data,data=meta,partial=True)
        if twitter_user_meta_data_serializer.is_valid(raise_exception=True):
            # pprint.pprint(twitter_user_meta_data_serializer.data)
            pprint.pprint(twitter_user_meta_data_serializer.validated_data)
            twitter_user_meta_data_serializer.save()

        next_token = meta.get('next_token',None)
        if next_token == None:
            meta.update(next_token='NO_TOKEN')
        tweets :  List = data.get('data')
        # print(tweets)
        for item in tweets:
            print(item)
            if len(item['text']) > 280:
                item['text'] = item['text'][:280]

            tweet,created = Tweet.objects.get_or_create(tweet_id = item.get('id'),twitter_user=twitter_user)
            tweet_serializer = TweetSerializer(instance=tweet,data={'text':item.get('text')},partial=True)
            
            if tweet_serializer.is_valid(raise_exception=True):
                 tweet_serializer.save()
            


                

def fetch_tweets_and_save_to_db(id,**kwargs):
    '''
    fetch the tweets of twitter user 

    params:
        id (int) : the id of twitter user
        
         pagination_token (str): for getting remaining tweets 
        from the list
        NOTE:use pagination_token : as next_token

        since_id (str) : from this tweet id to latest tweet 
        NOTE: use this for fetching latest tweet
        
    '''
    tweet_api = TweetAPI()
    try:
        twitter_user = TwitterUser.objects.get(user_id = id)
        twitter_user_meta_data=TwitterUserMetaData.objects.get(twitter_user = twitter_user)
    except ObjectDoesNotExist as e:
        while True:
            try: 
                data =  tweet_api.get_tweets(id)
                save_tweets(id,data)
                break
            except ConnectionError as e:
                sleep(5)
                print("connection error")
                continue
                    
                
        


    else:
        while True:
            try:
                if twitter_user_meta_data.next_token == 'NO_TOKEN':
                    data =  tweet_api.get_tweets(id)
                else: 
                    data = tweet_api.get_tweets(id,pagination_token=twitter_user_meta_data.next_token)
                save_tweets(id,data)
                break
            except ConnectionError as e:
                sleep(5)
                print("connection error")
                continue
       
        
        
