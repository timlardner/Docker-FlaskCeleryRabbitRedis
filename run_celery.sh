#!/bin/sh

cd app  

# run Celery worker for our project myproject
su -m app -c "celery -A tasks.celery worker --loglevel INFO"  