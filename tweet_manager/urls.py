from rest_framework import routers
from .views import TweetReadOnlyViewSet,TwitterUserReadOnlyViewSet
router = routers.DefaultRouter()

router.register('tweet',viewset=TweetReadOnlyViewSet,basename='tweet')
router.register('twitter-user',viewset=TwitterUserReadOnlyViewSet,basename='twitter-user')

urlpatterns = router.urls