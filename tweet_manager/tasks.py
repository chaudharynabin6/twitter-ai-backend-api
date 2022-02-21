import imp
from time import sleep
from celery import shared_task

# local import



@shared_task(bind=True)
def test_funcion(self):
    # local import
    from UserManager.models import TwitterUser
    from .controller.fetch_tweets import fetch_tweets_and_save_to_db


    while True:
        analysable_users = TwitterUser.objects.filter(isAnalysing=True,protected=False)
        for item in analysable_users:
            fetch_tweets_and_save_to_db(id=item.user_id)
        
        sleep(20)

    return 'Task Completed'

