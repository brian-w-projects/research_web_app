from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, DateField, SelectField, PasswordField, TextAreaField


class NewSessionForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[validators.DataRequired()])
    date = DateField('Date of Session ', format='%m/%d/%Y', validators=[validators.DataRequired()])
    form_name = SelectField('Select Data', choices=[('A', 'Session Self Report')],
                            validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class UpdatePatientForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class GeneralIntakeForm(FlaskForm):
    patient_id = StringField('Patient Id')
    date_of_birth = DateField('Date of Birth', format='%m/%d/%Y')
    eyes = SelectField('Eyes During Treatment', choices=[('', 'Answer Here'),
                                                         ('closed', 'Closed'), ('open', 'Open')])
    guardian_names = TextAreaField('Parents or Guardian Names')
    custody = TextAreaField('Custody')
    gender = SelectField('Gender', choices=[('','Answer Here'), ('male', 'Male'),
                                            ('female', 'Female'), ('other', 'Other')])
    address = TextAreaField('Address')
    phone = StringField('Phone Number')
    email = StringField('Email Address')
    handed = SelectField('Dominate Hand', choices=[('','Answer Here'), ('right', 'Right'),
                                                   ('left', 'Left'), ('both', 'Both')])
    diagnosis = TextAreaField('Previous and Current Diagnosis')
    reason_for_treatment = TextAreaField('Reason For Treatment')
    current_medication = TextAreaField('Current Medication (generic name, dosage, time of day)')
    previous_medication = TextAreaField('Previous Medication (generic name, dosage, time of day)')
    referral = TextAreaField('Source of Referral')
    general_submit = SubmitField('Submit')


class NewUserForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[validators.DataRequired()])
    first = StringField('First', validators=[validators.DataRequired()])
    last = StringField('Last', validators=[validators.DataRequired()])
    group = SelectField('Group', choices=[('1','Child Study Research'),('2','Clinical'),('3','Future Study')],
                        validators=[validators.DataRequired()])
    dob = DateField('Date of Birth', format='%m/%d/%Y', validators=[validators.DataRequired()])
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