#!/bin/bash

celery -A transcoder_celery_with_django worker -l INFO -P threads --autoscale=6,3
#celery -A transcoder_celery_with_django worker -l INFO -P eventlet