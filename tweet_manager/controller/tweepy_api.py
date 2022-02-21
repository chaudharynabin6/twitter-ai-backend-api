from logging import raiseExceptions
from typing import Dict
import tweepy
from tweepy import Client
from tweepy.errors import NotFound,TweepyException
from requests.exceptions import ConnectionError
import os
import sys
import pprint
from dotenv import load_dotenv

from datetime import datetime,timezone
from datetime import datetime
# local packages
# no local packages
# get 1 month ahead timestamp
# https://stackoverflow.com/questions/3424899/return-datetime-object-of-previous-month
def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and (not y%100==0 or y%400 == 0) else 28,
        31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)

# formating in RFC 3339 date format
def get_last_month():
    local_time = datetime.now(timezone.utc).astimezone()
    month_earlier = monthdelta(local_time,-1)
    print(month_earlier)
    str_rep = month_earlier.strftime('%Y-%m-%dT%H:%M:%S')
    return str_rep + 'Z'

dotenv_path = os.getcwd()
#ERROR: 
# https://docs.python.org/3/library/sys.html#sys.platform
# checking the os
if 'win' in sys.platform:
    dotenv_path = os.path.join(dotenv_path,"tweet_manager\controller\.env")
else:
    dotenv_path = os.path.join(dotenv_path,"tweet_manager/controller/.env")

print(dotenv_path)
load_dotenv(dotenv_path=dotenv_path)
bearer_token = os.getenv("bearer_token")
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class TweetAPI:
    '''
    Tweet class is responsible for only handling the tweets of the given user_id
    The whole process is automatic just pass the user_id then it will get all necessary tweets
    '''

    '''
    TODO:
    get tweet:
        [✔] fetch tweet of given user
        [✔] fetch tweet of given user from given tweet id to later
        [✔] fetch only of given max limit  and don't fetch from pagination
        [✔] wait for quota full
        [] raise exception of no more tweets
        [✔] raise excetion fo network error
    
    get twitter user:
        [✔] fetch all detail of twitter user
        [✔] raise exception if not found
        [✔] raise exception for network error
    '''
    
    def __init__(self) -> None:
        
        self.client = Client(return_type=dict,wait_on_rate_limit=True,bearer_token=bearer_token,consumer_key=consumer_key,consumer_secret=consumer_secret,access_token=access_token,access_token_secret=access_token_secret)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        self.api = api
    
    # get the detail fo twitter user through the sceen_name
    def get_user_detail(self,screen_name:str) -> str:
        try: 
            return self.api.get_user(screen_name=screen_name)._json
        except NotFound as e :
            raise Exception({
                'err':'TWITTER_USER_NOT_FOUND',
                'detail': 'please check screen name'
            })
        except TweepyException as e:
            raise Exception({
                'err': 'CONNECTION_ERROR',
                'detail': e
            })
    # Client.get_users_tweets(id, *, user_auth=False, end_time, exclude, expansions, max_results, media_fields, pagination_token,
    #  place_fields, poll_fields, since_id, start_time, tweet_fields, until_id, user_fields)
    # https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_users_tweets
    def get_tweets(self,twitter_id : str,**kwargs) -> Dict:
        '''
        since, this method is called with all the parameter from outside you don't need to fill all
        
        Only the 3200 most recent Tweets are available.
        parameters:
            id (str) : twitter id of user
            
            optional:
                max_results(int): how many tweet to return

                pagination_token (str): for getting remaining tweets 
                from the list
                NOTE:use pagination_token : as next_token

                since_id (str) : from this tweet id to latest tweet 
                NOTE: use this for fetching latest tweet
                
                until_id (str) : most recent tweet id to older tweets
                NOTE: use this for fetching older tweets

                start_time (Union[datetime.datetime, str]) –
                use start_time with a month ago 
                YYYY-MM-DDTHH:mm:ssZ (ISO 8601/RFC 3339).
                The oldest or earliest UTC timestamp from which 
                the Tweets will be provided. 
                Only the 3200 most recent Tweets are available.
                Timestamp is in second granularity and is inclusive
                (for example, 12:00:01 includes the first second of 
                the minute). 
                Minimum allowable time is 2010-11-06T00:00:00Z
                NOTE: Please note that this parameter does not
                support a millisecond value.
                

        returns:
            tweets ( dict) : dict containing all tweets and some meta data            
        '''
        
        
        if kwargs:
            # get paginated tweets
            tweets=  self.client.get_users_tweets(id=twitter_id, **kwargs)
            
        
        # get month ago tweets
        else:
            tweets = self.client.get_users_tweets(id=twitter_id,start_time=get_last_month(),**kwargs)
        data = tweets.get('data',None)
        meta = tweets.get('meta',None)
        if  data is None and meta is None : 
            raise Exception({
                'err': 'TWITTER_USER_NOT_FOUND',
                'detail': 'please check twitter_id'
            })
        return tweets

    


def main():
    #NOTE: algo how to fetch using pagination token to fetch earlier
    tweet = TweetAPI()
    # tweets = tweet.get_tweets(44196397,until_id = 1468938104446894092)
    tweets = tweet.get_tweets(44196397,until_id = 1468840273849589762)

    # tweets = tweet.get_tweets(44196397,since_id = )
    # tweets = tweet.get_tweets( 44196397,pagination_token='7140dibdnow9c7btw3z3b2647ln50kjowud35zhaku2i8')
    # user = tweet.get_user_detail('elonmusk')
    # tweets = tweet.get_tweets('1')
    # user = tweet.get_user_detail('xyxflkjdlfj')
    # pprint.pprint(user)
    pprint.pprint(tweets)


# oldest_id = 1468684576407101440
# newest_id = 1468938104446894092

#newest_id = 1468661470619738115
#oldest_id = 1468337774407340043
if __name__ == '__main__':
    main()