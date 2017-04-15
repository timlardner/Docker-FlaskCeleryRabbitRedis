# Flask-Celery-Rabbit-Redis for the WJ project

### Usage

    docker-compose build
    docker-compose up

To run multiple celery clients, do:

    docker-compose scale=N

where N is the desired number of backend worker nodes.

Then visit http://localhost:5000 for a demo
