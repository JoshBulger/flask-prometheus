from flask import Flask, render_template, redirect, url_for
from prometheus_client import generate_latest, REGISTRY, Counter, Gauge, Histogram
from survey.form import SurveyForm


def random_key():
    import random
    import string
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32))


application = Flask(__name__)
application.config['SECRET_KEY'] = random_key()


REQUESTS = Counter('http_requests_total', 'Total HTTP Requests (count)', ['method', 'endpoint', 'status_code'])
IN_PROGRESS = Gauge('http_requests_inprogress', 'Number of in progress HTTP requests')
TIMINGS = Histogram('http_request_duration_seconds', 'HTTP request latency (seconds)')
RESULTS = Counter('form_results', 'Response counter per question', ['question', 'answer'])


@application.route('/')
@TIMINGS.time()
@IN_PROGRESS.track_inprogress()
def index():
    REQUESTS.labels(method='GET', endpoint='/', status_code=200).inc()
    return render_template('index.html')


@application.route('/form', methods=['GET', 'POST'])
@TIMINGS.time()
@IN_PROGRESS.track_inprogress()
def form():
    REQUESTS.labels(method='GET', endpoint='/form/', status_code=200).inc()
    local_form = SurveyForm()
    if local_form.validate_on_submit():
        RESULTS.labels(question='role', answer=local_form.user_role.data).inc()
        RESULTS.labels(question='prometheus_experience', answer=local_form.prom_used.data).inc()
        RESULTS.labels(question='prometheus_learning', answer=local_form.prom_case.data).inc()
        RESULTS.labels(question='prometheus_in_use', answer=local_form.prom_using.data).inc()
        RESULTS.labels(question='promehteus_metrics_exposed', answer=local_form.prom_metrics.data).inc()
        RESULTS.labels(question='grafana_in_use', answer=local_form.grafana_using.data).inc()
        RESULTS.labels(question='grafana_experience', answer=local_form.grafana_used.data).inc()
        return redirect(url_for('training'))
    return render_template('form.html', form=local_form)


@application.route('/metrics')
@IN_PROGRESS.track_inprogress()
@TIMINGS.time()
def metrics():
    REQUESTS.labels(method='GET', endpoint="/metrics", status_code=200).inc()
    return generate_latest(REGISTRY)


@application.route('/training')
@IN_PROGRESS.track_inprogress()
@TIMINGS.time()
def training():
    REQUESTS.labels(method='GET', endpoint="/training", status_code=200).inc()
    return render_template('training.html')


@application.errorhandler(404)
@TIMINGS.time()
@IN_PROGRESS.track_inprogress()
def page_not_found(e):
    REQUESTS.labels(method='GET', endpoint='404', status_code=400).inc()
    return render_template('404.html', e=e), 404


if __name__ == "__main__":
    import os
    application.run(
        host='0.0.0.0',
        debug=True
    )
