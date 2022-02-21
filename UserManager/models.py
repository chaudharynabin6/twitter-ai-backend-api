from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class TwitterUser(models.Model):

    # user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    
    verified =              models.BooleanField(default=False)
    url=                    models.URLField(default="http://",blank=True)
    description =           models.TextField(default="",blank=True)
    user_id =               models.TextField(default="",blank=False)
    username =              models.CharField(max_length=255)
    protected =             models.BooleanField(default=False,blank=True)
    profile_image_url =     models.URLField(default="http://",blank=True)
    name =                  models.CharField(max_length=255,default="",blank=True)
    created_at =            models.DateTimeField(blank=True,null=True)
    isAnalysing =           models.BooleanField(default=False,blank=False)