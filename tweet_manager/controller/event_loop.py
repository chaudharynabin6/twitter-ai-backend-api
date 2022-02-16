# you should implement multi threading here
from .events import TweetFetcherEventEmitters
import asyncio
'''
TODO: 
    [] create the event loop for tweet fetcher
'''
task_queue = []
async def task_creator():
    tweet_fetcher_event_emitter = TweetFetcherEventEmitters()
    fetch_complete = True
    while fetch_complete:
        fetch = asyncio.create_task(tweet_fetcher_event_emitter.fetch_tweet())
        fetch_complete = True
        
async def main():
    tasks=[1,2,3,4,5,0,1,2,3,4]