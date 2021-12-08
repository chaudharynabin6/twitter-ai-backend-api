from typing import Dict
from rest_framework import serializers
import tweepy
from tweepy import Client
import os

from tweepy import client
from tweepy import user
from dotenv import load_dotenv
from pathlib import Path


dotenv_path = os.getcwd()
dotenv_path = os.path.join(dotenv_path,"tweet_manager/.env")
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

class Tweet:
    '''
    Tweet class is responsible for only handling the tweets of the given user_id
    The whole process is automatic just pass the user_id then it will get all necessary tweets
    '''
    
    def __init__(self) -> None:
        
        self.client = Client(bearer_token=bearer_token,consumer_key=consumer_key,consumer_secret=consumer_secret,access_token=access_token,access_token_secret=access_token_secret)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        self.api = api
    def get_user_id(self,screen_name:str) -> str:
        return self.api.get_user(screen_name=screen_name).id

    def getTweets(self,user) -> Dict:
        tweets = self.client.get_users_tweets(id=user.id,since_id=user.since_id)
        return tweets.data

def main():
    tweet = Tweet()
    tweet.getTweets()