
# pipdeptree

``` bash
python -m pipdeptree -f --exclude pip,pipdeptree,setuptools,wheel > locked-requirements.txt
```

# celery task
```bash
celery -A sentimental_analysis_on_celibrity_tweets.celery worker -l info
```

# celery previous task
```
celery -A sentimental_analysis_on_celibrity_tweets.celery purge -f
```
note: please install redis on your system follow [this link](https://redis.io/download)


# run project
open terminal in home directory and then open 4 tabs and use these commands

tab 1
```
cd projects/final_project_api_dev/
redis-server
```

tab2
```
cd projects/final_project_api_dev/
source venv/bin/activate
python manage.py runserver

```

tab3
```
cd projects/final_project_api_dev/
source venv/bin/activate
celery -A sentimental_analysis_on_celibrity_tweets.celery purge -f
celery -A sentimental_analysis_on_celibrity_tweets.celery worker -l info

```

tab4
```
cd projects/twittterai-frontend/
npm start
```


