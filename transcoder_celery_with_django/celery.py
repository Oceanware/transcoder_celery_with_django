import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcoder_celery_with_django.settings')

if os.name == "nt":
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('transcoder_celery_with_django')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task()
def add(x, y):
    return x + y