from typing import Any
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404

#local import
from .models import Tweet
from .serializers import TweetSerializer
from UserManager.models import TwitterUser

# code starts
class TweetReadOnlyViewSet(viewsets.ModelViewSet):

    def __init__(self, **kwargs: Any) -> None:
        self.queryset = Tweet.objects.all()
        self.serializer_class = TweetSerializer
        super().__init__(**kwargs)


@api_view(['GET','PATCH'])
def analysed_tweet(request,user=None):

    if request.method == "GET":

        if user != None:

       
            try:
                twitter_user = TwitterUser.objects.get(user_id=user,isAnalysing=True)
            
            except TwitterUser.DoesNotExist : 
                raise NotFound(detail={"analysing twitter user not found"})
            # twitter_user = get_object_or_404(TwitterUser,user_id = user,isAnalysing = True)
            analysed_tweets=Tweet.objects.filter(twitter_user=twitter_user,is_analysed=True)

            serialized_tweets= TweetSerializer(instance=analysed_tweets,many=True)

           

            return Response(data=serialized_tweets.data,status=status.HTTP_200_OK)
        else:
            raise NotFound(detail={"pass user first"})
            
            
            

            

