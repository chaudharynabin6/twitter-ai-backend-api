from typing import Any
from .models import Tweet,TwittterUser
from .serializers import TweetSerializer,TwitterUserSerializer
from rest_framework import viewsets

class TweetReadOnlyViewSet(viewsets.ModelViewSet):

    def __init__(self, **kwargs: Any) -> None:
        self.queryset = Tweet.objects.all()
        self.serializer_class = TweetSerializer
        super().__init__(**kwargs)

class TwitterUserReadOnlyViewSet(viewsets.ModelViewSet):
    
    def __init__(self, **kwargs: Any) -> None:
        self.queryset = Tweet.objects.all()
        self.serializer_class = TwitterUserSerializer
        super().__init__(**kwargs)
