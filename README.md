# transcoder_celery_with_django

Transcoder Celery With Django


## Steps

Run redis server port 6739 (default port)
```shell 
redis-server
```

Run celery workers
```shell 
sh .\celery-progress.sh
```

```shell 
sh .\celery-run.sh

```

Run django server
```shell 
python3 manage.py runserver
```