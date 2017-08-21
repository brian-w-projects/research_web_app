from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, TextAreaField, DateField, SelectField


class NewSessionForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[validators.DataRequired()])
    first_name = StringField('First Name', validators=[validators.DataRequired()])
    last_name = StringField('Last Name', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class IdentifyAssessmentForm(FlaskForm):
    assessment = StringField('Session', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class GeneralIntake(FlaskForm):
    patient_id = StringField('Patient Id')
    date_of_birth = DateField('Date of Birth', format='%m/%d/%Y')
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
    submit = SubmitField('Submit')