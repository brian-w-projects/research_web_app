from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, SelectField, BooleanField


class NewTokenForm(FlaskForm):
    first = StringField('First', validators=[validators.DataRequired()])
    last = StringField('Last', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class NewUserForm(FlaskForm):
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