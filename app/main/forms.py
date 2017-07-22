from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField


class TokenForm(FlaskForm):
    token = StringField('Token', validators=[validators.DataRequired()])
    first_name = StringField('First Name', validators=[validators.DataRequired()])
    last_name = StringField('Last Name', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')