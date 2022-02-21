from rest_framework import routers
from .views import TweetReadOnlyViewSet
router = routers.DefaultRouter()

router.register('tweet',viewset=TweetReadOnlyViewSet,basename='tweet')

urlpatterns = router.urls