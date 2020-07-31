import random, time

from flask import Flask, render_template_string, abort
from prometheus_client import generate_latest, REGISTRY, Counter, Gauge, Histogram

application = Flask(__name__)

REQUESTS = Counter('http_requests_total', 'Total HTTP Requests (count)', ['method', 'endpoint', 'status_code'])
IN_PROGRESS = Gauge('http_requests_inprogress', 'Number of in progress HTTP requests')
TIMINGS = Histogram('http_request_duration_seconds', 'HTTP request latency (seconds)')

@application.route('/')
@TIMINGS.time()
@IN_PROGRESS.track_inprogress()
def hello_world():
    REQUESTS.labels(method='GET', endpoint='/', status_code=200).inc()
    return 'Hello World!'

@application.route('/hello/<name>')
@TIMINGS.time()
@IN_PROGRESS.track_inprogress()
def index(name):
    REQUESTS.labels(method='GET', endpoint='/hello/', status_code=200).inc()
    return render_template_string('<b>Hey {{name}}, welcome to this simple demo app!</b>', name=name)

@application.route('/metrics')
@IN_PROGRESS.track_inprogress()
@TIMINGS.time()
def metrics():
    REQUESTS.labels(method='GET', endpoint="/metrics", status_code=200).inc()
    return generate_latest(REGISTRY)


@application.errorhandler(404)
@TIMINGS.time()
@IN_PROGRESS.track_inprogress()
def page_not_found(e):
    REQUESTS.labels(method='GET', endpoint='404', status_code=400).inc()
    # note that we set the 404 status explicitly
    return render_template_string('Page Not Found!'), 404


if __name__ == "__main__":
    application.run(host='0.0.0.0')
