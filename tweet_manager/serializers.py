from django.db import models
from rest_framework import serializers
from .models import Tweet,TwittterUser,TwitterUserMetaData

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = '__all__'


class TwitterUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TwittterUser
        fields = '__all__'


class TwitterUserMetaDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = TwitterUserMetaData
        fields = '__all__'