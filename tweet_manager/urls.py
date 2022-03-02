from django.urls import path


from rest_framework import routers
from .views import TweetReadOnlyViewSet,analysed_tweet,total_summary,time_series_summary
from .views import all_user_summary
router = routers.DefaultRouter()

router.register('tweet',viewset=TweetReadOnlyViewSet,basename='tweet')

urlpatterns = router.urls

urlpatterns += [
    path(r'analysed-tweets/<int:user>',view = analysed_tweet),
    path(r'total-summary/<int:user>',view = total_summary),
    path(r'time-series-summary/<int:user>',view = time_series_summary),
    path(r'all-user-summary/',view = all_user_summary) 


]