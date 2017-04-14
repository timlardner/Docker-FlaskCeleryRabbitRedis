# See README.me for install and usage instructions

import os
import uuid
import random
import string
import time
import json
import datetime
from io import BytesIO

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from flask import Flask, request, redirect, flash, url_for, session, g
from flask import render_template, render_template_string
from flask import Blueprint, make_response, abort
from celery import Celery, current_task
from celery.result import AsyncResult

# Get backend info from environment variables
REDIS_PORT = 6379  
REDIS_DB = 0  
REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR', 'redis')
REDIS_URL = 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT, REDIS_DB)

# Get broker info from environment variables
RABBIT_HOSTNAME = os.environ.get('RABBIT_PORT_5672_TCP', 'rabbit')
if RABBIT_HOSTNAME.startswith('tcp://'):  
    RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]
BROKER_URL = os.environ.get('BROKER_URL','')
if not BROKER_URL:  
    BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
        user=os.environ.get('RABBIT_ENV_USER', 'admin'),
        password=os.environ.get('RABBIT_ENV_RABBITMQ_PASS', 'mypass'),
        hostname='rabbit',
        vhost=os.environ.get('RABBIT_ENV_VHOST', ''))

print(BROKER_URL)

app = Flask(__name__)
celery = Celery(app.name,
        backend=REDIS_URL,
        broker=BROKER_URL)

celery.conf.accept_content = ['json', 'msgpack']
celery.conf.result_serializer = 'msgpack'

@celery.task()
def get_data_from_strava():
    current_task.update_state(state='PROGRESS', meta={'current':0.1})
    time.sleep(2)
    current_task.update_state(state='PROGRESS', meta={'current':0.3})
    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    current_task.update_state(state='PROGRESS', meta={'current':0.5})
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    current_task.update_state(state='PROGRESS', meta={'current':0.8})
    png_output = BytesIO()
    canvas.print_png(png_output)
    out = png_output.getvalue()
    return out

@app.route('/progress')
def progress():
    jobid = request.values.get('jobid')
    if jobid:
        job = AsyncResult(jobid, app=celery)
        if job.state == 'PROGRESS':
            return json.dumps(dict(
                state = job.state,
                progress = job.result['current'],
            ))
        elif job.state == 'SUCCESS':
            return json.dumps(dict(
                state = job.state,
                progress = 1.0,
            ))
    return '{}'

@app.route('/result.png')
def result():
    jobid = request.values.get('jobid')
    if jobid:
        job = AsyncResult(jobid, app=celery)
        png_output = job.get()
        response = make_response(png_output)
        response.headers['Content-Type'] = 'image/png'
        return response
    else:
        return 404

@app.route('/image_page')
def image_page():
    job = get_data_from_strava.delay()
    return render_template_string('''\
<style>
#prog {
width: 400px;
border: 1px solid red;
height: 20px;
}
#bar {
width: 0px;
background-color: blue;
height: 20px;
}
</style>
<h3>Awesome Asynchronous Image Generation</h3>
<div id="imgpl">Image not ready. Please wait.</div>
<div id="wrapper"><div id="prog"><div id="bar"></div></div></div>
<script src="//code.jquery.com/jquery-2.1.1.min.js"></script>
<script>
function poll() {
    $.ajax("{{url_for('.progress', jobid=JOBID)}}", {
        dataType: "json"
        , success: function(resp) {
            $("#bar").css({width: $("#prog").width() * resp.progress});
            if(resp.progress >= 0.99) {
                $("#wrapper").html('');
                $("#imgpl").html('<img src="result.png?jobid={{JOBID}}">');

                
                return;
            } else {
                setTimeout(poll, 500.0);
            }

        }
    });

}

$(function() {
    var JOBID = "{{ JOBID }}";
    poll();

});
</script>
''', JOBID=job.id)


@app.route('/')
def index():
    return render_template_string('''\
<a href="{{ url_for('.image_page') }}">Whatever you click to get data from Strava...</a>
''')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
