import time
import random
import datetime

from io import BytesIO
from celery import Celery, current_task
from celery.result import AsyncResult
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

REDIS_URL = 'redis://redis:6379/0' 
BROKER_URL = 'amqp://admin:mypass@rabbit//'

celery = Celery('tasks',
        backend=REDIS_URL,
        broker=BROKER_URL)

celery.conf.accept_content = ['json', 'msgpack']
celery.conf.result_serializer = 'msgpack'

def get_job(ID):
    return AsyncResult(ID, app=celery)

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