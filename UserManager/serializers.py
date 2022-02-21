from dataclasses import field
from rest_framework import serializers
from . import models

class TwitterUserSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.TwitterUser
        # fields = [str(field.name) for field in models.TwitterUser._meta.fields]
        fields = "__all__"
        # extra_kwargs = {
        #     "verified": {"required": False},
        #     "url": {"required": False},
        #     "description": {"required": False},
        #     "user_id": {"required": True},
        #     "username": {"required": True},
        #     "protected": {"required": False},
        #     "profile_image_url": {"required": False},
        #     "name": {"required": False},
        #     "created_at": {"required": False},
        #     "isAnalysing": {"required": True},
        #     }