import os

from celery import Celery
from celery.schedules import crontab
# from . import periodic_tasks
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentimental_analysis_on_celibrity_tweets.settings')

app = Celery('sentimental_analysis_on_celibrity_tweets')

app.conf.update(timezone = 'Asia/Kathmandu')
app.conf.enable_utc = True
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# TODO: -------------CELERY BEAT SETTING ---------

# app.conf.beat_schedule = periodic_tasks.tasks
# --------------------------------------------------
# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# removing previous task 
app.control.purge()