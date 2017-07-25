from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, PasswordField


class RegisterForm(FlaskForm):
    first_name = StringField('First Name: ', validators=[validators.DataRequired()])
    last_name = StringField('Last Name: ', validators=[validators.DataRequired()])
    email = StringField('Email: ', validators=[validators.DataRequired(), validators.Email()])
    token = StringField('Token: ', validators=[validators.DataRequired()])
    password = PasswordField('Password: ', validators=[validators.DataRequired(),
                                                       validators.EqualTo('password_confirm'),
                                                       validators.Length(min=10)])
    password_confirm = PasswordField('Confirm: ', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password ', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class TokenForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    token = StringField('Token', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')