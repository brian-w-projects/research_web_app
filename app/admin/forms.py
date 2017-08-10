from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, DateField, SelectField, PasswordField, TextAreaField


class NewSessionForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[validators.DataRequired()])
    first = StringField('First Name', validators=[validators.DataRequired()])
    last = StringField('Last Name', validators=[validators.DataRequired()])
    date = DateField('Date of Session ', format='%m/%d/%Y', validators=[validators.DataRequired()])
    form_name = SelectField('Select Data', choices=[('A', 'Self Assessment')],
                            validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class NewUserForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[validators.DataRequired()])
    first = StringField('First', validators=[validators.DataRequired()])
    last = StringField('Last', validators=[validators.DataRequired()])
    group = SelectField('Group', choices=[('1','1'),('2','2'),('3','3')],
                        validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class NewResearcherForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    submit = SubmitField('Submit')


class RemoveResearcherForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    submit = SubmitField('Submit')


class NewPasswordForm(FlaskForm):
    current_password = PasswordField('Password', validators=[validators.DataRequired(),
                                                             validators.Length(min=10)])
    new_password = PasswordField('New Password', validators=[validators.DataRequired(),
                                                             validators.EqualTo('confirm_password'),
                                                             validators.Length(min=10)])
    confirm_password = PasswordField('Confirm Password', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    submit = SubmitField('Submit')


class ProtocolForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[validators.DataRequired()])
    form_id = StringField('Session', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')