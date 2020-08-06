from flask_wtf import FlaskForm
from wtforms import Form, RadioField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired


class SurveyForm(FlaskForm):
    user_role = RadioField('What is your role?',
                           choices=[('manager', "Management"),
                                    ('dev', "Developer"),
                                    ('admin', "SysAdmin"),
                                    ('sre', "SRE"),
                                    ('lead', "Tech or Team Lead"),
                                    ('other', "Other or Prefer not to say")])
    prom_used = RadioField('Have you ever used Prometheus before?',
                           choices=[('false', 'No'), ('true', 'Yes')])
    prom_using = RadioField("Are you currently using Prometheus?",
                            choices=[('false', "No"), ('true', "Yes")])
    prom_metrics = RadioField("Do you already have Prometheus metrics exposed?",
                              choices=[('false', "No"), ('true', 'Yes')])
    prom_case = RadioField("What do you most want to learn about Prometheus?",
                           choices=[('promql', "Metrics Queries"),
                                    ('metrics', "Exposing custom metrics"),
                                    ('dashboard', "Dashboards")])
    grafana_used = RadioField('Have you ever used Grafana before?',
                              choices=[('false', 'No'), ('true', 'Yes')])
    grafana_using = RadioField('Are you already using Grafana?',
                               choices=[('false', "No"), ('true', "Yes")])

    submit = SubmitField('Submit')
