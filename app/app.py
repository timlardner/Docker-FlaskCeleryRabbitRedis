# See README.md for install and usage instructions

import json
import tasks

from flask import Flask, request, url_for
from flask import render_template, make_response

app = Flask(__name__)

@app.route('/progress')
def progress():
    jobid = request.values.get('jobid')
    if jobid:
        job = tasks.get_job(jobid)
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
        job = tasks.get_job(jobid)
        png_output = job.get()
        response = make_response(png_output)
        response.headers['Content-Type'] = 'image/png'
        return response
    else:
        return 404

@app.route('/image_page')
def image_page():
    job = tasks.get_data_from_strava.delay()
    return render_template('home.html', JOBID=job.id)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
