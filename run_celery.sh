#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

cd WJ  

# run Celery worker for our project myproject
su -m wj -c "celery -A wj.celery worker"  