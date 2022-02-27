from datetime import datetime
import django
from django.db import models

# local imports
from UserManager.models import TwitterUser
# Create your models here.

# class TwittterUser(models.Model):
#     created_at = models.DateTimeField()
#     description = models.TextField(max_length=280)
#     favourites_count = models.PositiveBigIntegerField()
#     followers_count = models.PositiveBigIntegerField()
#     friends_count = models.PositiveBigIntegerField()
#     # use twiter_id
#     twitter_id = models.PositiveBigIntegerField()
#     lang = models.CharField(max_length=50)
#     listed_count = models.PositiveBigIntegerField()
#     location = models.CharField(max_length=280)
#     name = models.CharField(max_length=280)
#     profile_background_image_url = models.URLField(max_length=280)
#     profile_background_image_url_https = models.URLField(max_length=280)
#     profile_banner_url = models.URLField(max_length=500)
#     profile_banner_url_https = models.URLField(max_length=500)
#     screen_name = models.CharField(max_length=280)
#     verified = models.BooleanField()
    


class Tweet(models.Model):
    tweet_id = models.PositiveBigIntegerField()
    text = models.CharField(max_length=280)
    twitter_user = models.ForeignKey(TwitterUser,on_delete=models.CASCADE,related_name='twitter_user_for_tweet')
    is_analysed = models.BooleanField(default=False)
    label = models.CharField(max_length=100,default="NOT_CLASSIFIED")
    score = models.FloatField(default=0)


class TwitterUserMetaData(models.Model):
    newest_id = models.PositiveBigIntegerField(default=0)
    oldest_id = models.PositiveBigIntegerField(default=0)
    result_count = models.IntegerField(default=0)
    next_token = models.CharField(max_length=100,default='NO_TOKEN')
    previous_token = models.CharField(max_length=100,default='NO_TOKEN')
    twitter_user = models.ForeignKey(TwitterUser,on_delete=models.CASCADE,related_name='twitter_user_for_meta_data')

class TotalSummary(models.Model):
    twitter_user = models.ForeignKey(TwitterUser,on_delete=models.CASCADE,related_name='twitter_user_for_total_summary')
    positive = models.PositiveBigIntegerField(default=0)
    negative = models.PositiveBigIntegerField(default=0)
    total = models.PositiveBigIntegerField(default=0)


class TimeSeriesSummary(models.Model):
    twitter_user = models.ForeignKey(TwitterUser,on_delete=models.CASCADE,related_name='twitter_user_for_time_series_summary')
    position = models.SmallIntegerField(default=0)
    positive = models.PositiveBigIntegerField(default=0)
    negative = models.PositiveBigIntegerField(default=0)
    total = models.PositiveBigIntegerField(default=0)
    date = models.DateTimeField(default=datetime.now())