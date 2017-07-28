from flask import render_template, request, flash, redirect, url_for, abort, current_app, send_file, Response
from . import data
from .forms import SingleDataForm
from ..models import Form
from bleach import clean
from flask_login import login_required
from datetime import datetime, timedelta
from sqlalchemy.sql.expression import or_, desc


@data.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = SingleDataForm(request.form)
    if request.method == 'POST':
        id = clean(form.patient_id.data)
        initial = clean(form.initial_data.data)
        dates = clean(form.data_request.data)
        form_type = clean(form.form_type.data)
        if form.validate():
            form_process = get_forms(get_date_reference(dates), initial, form_type, id)
            if len(form_process) == 0:
                flash(u'No data from this search', 'error')
                return redirect(url_for('data.index'))
            csv = 'Date,'
            questions = len([y for x in Form.get_questions(form_type) for y in x])
            for i in range(1,questions+1):
                csv += "{0}i,{0}f,{0}c,{0}n,".format(str(i))
            csv += '\n'
            for single_form in form_process:
                csv += '{}'.format(single_form.date)[:10] + ','
                for q in single_form.question:
                    csv += "{},{},{},{},".format(q.intensity, q.frequency, q.change, q.notes)
                csv += '\n'
            headers = {'Content-disposition': 'attachment; filename={}.csv'.format(str(id))}
            return Response(csv, mimetype='text/csv', headers=headers)
        else:
            flash(u'Please check form', 'error')
            return redirect(url_for('data.index'))
    return render_template('data/index.html', form=form)


def get_forms(reference_date, initial, form_type, id):
    form_query = Form.query \
        .filter(Form.patient_id == id,
                Form.name == form_type)
    initial_form = form_query.from_self() \
            .order_by(Form.date) \
            .first().id if initial else -1
    if reference_date:
        return form_query.from_self() \
                    .filter(or_(Form.date > reference_date,
                                Form.id == initial_form)) \
                    .order_by(Form.date)\
                    .all()
    else:
        most_recent = form_query.from_self() \
            .order_by(desc(Form.date))\
            .first().id
        return form_query.from_self() \
            .filter(or_(Form.id == initial_form,
                        Form.id == most_recent))\
            .all()


def get_date_reference(dates):
    today = datetime.today()
    return {
        'all' : str(today - timedelta(days=10000)),
        '12' : str(today - timedelta(days=365)),
        '6' : str(today - timedelta(days=183)),
        '3' : str(today - timedelta(days=90)),
        '1' : str(today - timedelta(days=31)),
    }.get(dates, '')