from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, BooleanField, DateField


class NewSessionForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[validators.DataRequired()])
    first = StringField('First Name', validators=[validators.DataRequired()])
    last = StringField('Last Name', validators=[validators.DataRequired()])
    form_name = StringField('Form Name', validators=[validators.DataRequired()])
    date = DateField('Date of Session ', format='%m/%d/%Y', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class NewUserForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[validators.DataRequired()])
    first = StringField('First', validators=[validators.DataRequired()])
    last = StringField('Last', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class NewResearcherForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    submit = SubmitField('Submit')


class RemoveResearcherForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    confirm = BooleanField('Confirm: ', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')