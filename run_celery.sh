#!/bin/sh

cd WJ  

# run Celery worker for our project myproject
su -m wj -c "celery -A wj.celery worker --loglevel INFO	"  