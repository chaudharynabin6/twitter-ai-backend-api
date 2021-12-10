from django.db import models
from rest_framework import serializers
from .models import Tweet,TwittterUser

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = '__all__'


class TwitterUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TwittterUser
        fields = '__all__'