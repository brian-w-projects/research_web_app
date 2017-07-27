from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, BooleanField, SelectField


class SingleDataForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[validators.DataRequired()])
    initial_data = BooleanField('Initial Data')
    form_type = SelectField('Select Form', choices=[('A', 'A'), ('B', 'B'), ('C', 'C')],
                            validators=[validators.DataRequired()])
    data_request = SelectField('Select Data', choices=[('all', 'All Records'), ('12', 'Last Calender Year'),
                                                       ('6', 'Last 6 Months'), ('3', 'Last 3 Months'),
                                                       ('1', 'Last Month'), ('recent', 'Most Recent')],
                               validators=[validators.DataRequired()])
    submit = SubmitField('Submit')