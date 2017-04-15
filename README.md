# Using Celery with Flask for Asynchronous Content Generation

This tutorial explains how to configure Flask, Celery, RabbitMQ and Redis, together with Docker to build a web service that dynamically generates content and loads this contend when it is ready to be displayed. We'll focus mainly on Celery and the servies that surround it. Docker is a bit more straitforward.

## Contents

1. [Part 1 - Project Structure](https://github.com/timlardner/Docker-FlaskCeleryRabbitRedis/tree/readme#part-1---project-structure)
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

## Part 2 - Creating the Flask application

First we create an folder for our app.

## Part 3 - Expanding our web app to use Celery

## Part 4 - Using Docker to package our application

Our app requires 4 separate containers for each of our servies:
* Flask
* Celery
* RabbitMQ
* Redis

Docker provides prebuilt containers for [RabbitMQ](https://hub.docker.com/_/rabbitmq/) and [Redis](https://hub.docker.com/_/redis/). These both work well and we'll use them as is.

For Flask and Celery, we'll build two identical containers from a simple `Dockerfile`.

```
# Pull the latest version of the Python container.
FROM python:latest

# Add the requirements.txt file to the image.
ADD requirements.txt /app/requirements.txt

# Set the working directory to /app/.
WORKDIR /app/

# Install Python dependencies.
RUN pip install -r requirements.txt

# Create an unprivileged user for running our Python code.
RUN adduser --disabled-password --gecos '' app  
```

We pull all of this together with a Docker compose file, `docker-compose.yml`. While early versions of compose needed to expose ports for each service, we can link the services together using the `links` keyword. The `depends` keyword ensures that all of our services start in the correct order.

To create and run the container, use:

    docker-compose build
    docker-compose up

One of the major benefits of Docker is that we can run multiple instances of a container if required. To run multiple instances of our Celery consumers, do:

    docker-compose scale=N

where N is the desired number of backend worker nodes.

Visit http://localhost:5000 to view our complete application.
