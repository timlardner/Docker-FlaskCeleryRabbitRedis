''' See README.md for install and usage instructions '''

import json
from flask import Flask, request
from flask import render_template, make_response
import tasks

APP = Flask(__name__)

@APP.route('/progress')
def progress():
    '''
    Get the progress of our task and return it using a JSON object
    '''
    jobid = request.values.get('jobid')
    if jobid:
        job = tasks.get_job(jobid)
        if job.state == 'PROGRESS':
            return json.dumps(dict(
                state=job.state,
                progress=job.result['current'],
            ))
        elif job.state == 'SUCCESS':
            return json.dumps(dict(
                state=job.state,
                progress=1.0,
            ))
    return '{}'

@APP.route('/result.png')
def result():
    '''
    Pull our generated .png binary from redis and return it
    '''
    jobid = request.values.get('jobid')
    if jobid:
        job = tasks.get_job(jobid)
        png_output = job.get()
        response = make_response(png_output)
        response.headers['Content-Type'] = 'image/png'
        return response
    else:
        return 404

@APP.route('/image_page')
def image_page():
    '''
    Enqueue the image generation task and show the webpage
    '''
    job = tasks.get_data_from_strava.delay()
    return render_template('home.html', JOBID=job.id)

@APP.route('/')
def index():
    '''
    Our web app's entry point
    '''
    return render_template('index.html')

if __name__ == '__main__':
    APP.run(host='0.0.0.0')
