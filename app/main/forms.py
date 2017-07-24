from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField


class NewSessionForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[validators.DataRequired()])
    first_name = StringField('First Name', validators=[validators.DataRequired()])
    last_name = StringField('Last Name', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class IdentifyAssessmentForm(FlaskForm):
    assessment = StringField('Session', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')