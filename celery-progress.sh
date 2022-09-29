#!/bin/bash

celery -A transcoder_celery_with_django worker -l INFO --pool=solo -Q wsQ
