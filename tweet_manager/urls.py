from django.urls import path


from rest_framework import routers
from .views import TweetReadOnlyViewSet,analysed_tweet
router = routers.DefaultRouter()

router.register('tweet',viewset=TweetReadOnlyViewSet,basename='tweet')

urlpatterns = router.urls

urlpatterns += [
    path(r'analysed-tweets/<int:user>',view = analysed_tweet)
]