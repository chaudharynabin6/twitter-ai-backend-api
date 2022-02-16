# you should have all the events handler and trigger method here 


from pyee import AsyncIOEventEmitter
events = AsyncIOEventEmitter()
class TweetFetcherEventHandler():
    @events.on('fetch_tweets')
    async def fetch_tweet():
        pass

    @events.on('cancel')
    async def cancel():
        pass

    @events.on('new_twitter_user')
    async def new_twitter_user():
        pass

class TweetFetcherEventEmitters():
    
    async def fetch_tweet():
        events.emit('fetch_tweets')

    async def cancel():
        events.emit('cancel')

    async def new_twitter_user():
        events.emit('new_twitter_user')
        
