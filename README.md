
# pipdeptree

``` bash
python -m pipdeptree -f --exclude pip,pipdeptree,setuptools,wheel > locked-requirements.txt
```

# celery task
```bash
celery -A sentimental_analysis_on_celibrity_tweets.celery worker -l info
```
note: please install redis on your system follow [this link](https://redis.io/download)