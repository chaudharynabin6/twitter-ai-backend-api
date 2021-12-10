from django.db import models

# Create your models here.

class TwittterUser(models.Model):
    created_at = models.DateTimeField()
    description = models.TextField(max_length=280)
    favourites_count = models.PositiveBigIntegerField()
    followers_count = models.PositiveBigIntegerField()
    friends_count = models.PositiveBigIntegerField()
    # use twiter_id
    twitter_id = models.PositiveBigIntegerField()
    lang = models.CharField(max_length=50)
    listed_count = models.PositiveBigIntegerField()
    location = models.CharField(max_length=280)
    name = models.CharField(max_length=280)
    profile_background_image_url = models.URLField(max_length=280)
    profile_background_image_url_https = models.URLField(max_length=280)
    profile_banner_url = models.URLField(max_length=500)
    profile_banner_url_https = models.URLField(max_length=500)
    screen_name = models.CharField(max_length=280)
    verified = models.BooleanField()
    


class Tweet(models.Model):
    tweet_id = models.PositiveBigIntegerField()
    text = models.CharField(max_length=280)
    twitter_user = models.ForeignKey(TwittterUser,on_delete=models.CASCADE,related_name='twitter_user')

