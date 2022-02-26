import imp
from django.db import models
from rest_framework import serializers
# local imports
from .models import Tweet,TwitterUserMetaData,TotalSummary,TimeSeriesSummary

from UserManager.models import TwitterUser
class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = '__all__'


class TwitterUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TwitterUser
        fields = '__all__'


class TwitterUserMetaDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = TwitterUserMetaData
        fields = '__all__'

class TotalSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = TotalSummary
        fields = '__all__'

class TimeSeriesSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeSeriesSummary
        fields = '__all__'
