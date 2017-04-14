# Flask-Celery for WJ

### Usage

    sudo apt-get install rabbitmq-server
    curl http://download.redis.io/redis-stable.tar.gz | tar xz && cd redis-stable && make && sudo make install

Configure redis based on: https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04

    pip install celery
    pip install msgpack-python
    celery -A wj.celery worker
    python wj.py

Then visit http://localhost:5000 for a demo
