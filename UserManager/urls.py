
from django.urls import path

from . import views


urlpatterns= [

    path(route=r"user/",view=views.search_and_add_twitter_users),
    path(route=r"user/<str:users>",view=views.search_and_add_twitter_users),


]