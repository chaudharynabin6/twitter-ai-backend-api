from typing import Any
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404

#local import
from .models import Tweet,TotalSummary,TimeSeriesSummary
from .serializers import TweetSerializer,TotalSummarySerializer,TimeSeriesSummarySerializer
from UserManager.models import TwitterUser

# code starts
class TweetReadOnlyViewSet(viewsets.ModelViewSet):

    def __init__(self, **kwargs: Any) -> None:
        self.queryset = Tweet.objects.all()
        self.serializer_class = TweetSerializer
        super().__init__(**kwargs)


@api_view(['GET'])
def analysed_tweet(request,user=None):
    "analyse the tweet of given user"
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
            
            
            
@api_view(['GET'])
def total_summary(request,user = None):

    if request.method == 'GET':
        
        if user != None:
            try:
                twitter_user = TwitterUser.objects.get(user_id=user,isAnalysing=True)
            
            except TwitterUser.DoesNotExist : 
                raise NotFound(detail={"analysing twitter user not found"})
            
            try:
                total_summary = TotalSummary.objects.get(twitter_user=twitter_user)
                total_tweets_fetched = Tweet.objects.filter(twitter_user=twitter_user)
            except TotalSummary.DoesNotExist :
                raise NotFound(detail={"still processing total_summary for current user"})
            serialized_total_summary = TotalSummarySerializer(instance=total_summary)
            data = serialized_total_summary.data
            data['total_fetched'] = len(total_tweets_fetched)
            return Response(data=data,status=status.HTTP_200_OK)
        
        else:
            raise NotFound(detail="please supply >>twitter user id<<< in params")

            
            
@api_view(['GET'])
def time_series_summary(request,user = None):

    if request.method == 'GET':
        
        if user != None:
            try:
                twitter_user = TwitterUser.objects.get(user_id=user,isAnalysing=True)
            
            except TwitterUser.DoesNotExist : 
                raise NotFound(detail={"analysing twitter user not found"})
            
            
            time_series_summary = TimeSeriesSummary.objects.filter(twitter_user=twitter_user).order_by("position")
            if not time_series_summary.exists():
                raise NotFound(detail={"still processing time series summary for current user"})
            serialized_time_series_summary = TimeSeriesSummarySerializer(instance=time_series_summary,many=True)

            return Response(data=serialized_time_series_summary.data,status=status.HTTP_200_OK)
        
        else:
            raise NotFound(detail="please supply >>twitter user id<<< in params")

            
     
            
@api_view(['GET'])
def all_user_summary(request):

    if request.method == "GET":
        analysing_twitter_users = TwitterUser.objects.filter(isAnalysing=True,protected=False)

        data = []
        for user in analysing_twitter_users:

            all_analysed_tweets = Tweet.objects.filter(is_analysed=True,twitter_user = user)

            positive_tweets = all_analysed_tweets.filter(label="POSITIVE")

            n_all_analysed_tweets = len(all_analysed_tweets)

            n_positive_tweets = len(positive_tweets)

            n_negative_tweets = n_all_analysed_tweets - n_positive_tweets
            # calcualatin percentage
            # if(n_all_analysed_tweets > 0):
            #     n_negative_tweets = 100 * n_positive_tweets / n_all_analysed_tweets
            #     n_negative_tweets = 100 * n_negative_tweets / n_all_analysed_tweets
          
                

            
            single_user_summary = {
                'positive':n_positive_tweets,
                'negative':n_negative_tweets,
                'name':user.name
            }

            data.append(single_user_summary)
        
        return JsonResponse(data=data,status=status.HTTP_200_OK,safe=False)