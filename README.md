# Using Celery with Flask for Asynchronous Content Generation

This tutorial explains how to configure Flask, Celery, RabbitMQ and Redis, together with Docker to build a web service that dynamically generates content and loads this contend when it is ready to be displayed. We'll focus mainly on Celery and the servies that surround it. Docker is a bit more straitforward.

## Contents

1. Part 1 - Project Structure
1. Part 2 - Creating the Flask application
1. Part 3 - Expanding our web app to use Celery
1. Part 4 - Using Docker to package our application

## Part 1 - Project Structure

The finished project structure will be as follows:

- Project Root
	- README.md
	- requirements.txt
	- Dockerfile
	- docker-compose.yml
	- app
	    - templates
	        - home.html
	        - index.hmtl
	    - app.py
	    - tasks.py
	- scripts
	    - run_celery.sh
	    - run_web.sh

### Usage

    docker-compose build
    docker-compose up

To run multiple celery clients, do:

    docker-compose scale=N

where N is the desired number of backend worker nodes.

Then visit http://localhost:5000 for a demo
