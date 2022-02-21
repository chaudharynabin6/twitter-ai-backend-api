import imp
from django.db import models
from rest_framework import serializers
# local imports
from .models import Tweet,TwitterUserMetaData

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