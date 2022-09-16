#!/bin/bash

celery -A transcoder_celery_with_django worker -l INFO -P gevent
#celery -A transcoder_celery_with_django worker -l INFO -P eventlet