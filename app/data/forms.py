from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, BooleanField, SelectField


class SingleDataForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[validators.DataRequired()])
    initial_data = BooleanField('Initial Data')
    patient_data = BooleanField('Patient Data')
    intake_data = BooleanField('Intake Data')
    form_type = SelectField('Select Form', choices=[('A', 'A'), ('B', 'B'), ('C', 'C')],
                            validators=[validators.DataRequired()])
    data_request = SelectField('Select Data', choices=[('5', '5 most recent'), ('10', '10 most recent'),
                                                       ('15', '15 most recent'), ('20', '20 most recent'),
                                                       ('25', '25 most recent'), ('30', '30 most recent'),
                                                       ('40', '40 most recent'), ('50', '50 most recent'),
                                                       ('all', 'All records')],
                               validators=[validators.DataRequired()])
    submit = SubmitField('Submit')