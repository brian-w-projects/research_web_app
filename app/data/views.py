from flask import render_template, request, flash, redirect, url_for, Response
from . import data
from .forms import SingleDataForm
from ..models import Form, Question, Intake
from bleach import clean
from flask_login import login_required
from datetime import datetime, timedelta
from sqlalchemy.sql.expression import or_, desc
import flask_excel as excel


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
            form_process = get_forms(dates, initial, form_type, id)
            if len(form_process) == 0:
                flash(u'No data from this search', 'error')
                return redirect(url_for('data.index'))
            return excel.make_response_from_book_dict(get_xls(form_process, form_type, form.patient_data.data,
                                                              form.intake_data.data), 'xls',
                                                      file_name=id)
        else:
            flash(u'Please check form', 'error')
            return redirect(url_for('data.index'))
    return render_template('data/index.html', form=form)


def get_xls(process, form_type, patient_data, intake_data):
    to_ret = {}
    header = ['Patient', 'Group', 'Session', 'Date']
    header.extend([y for x in Form.get_questions(form_type) for y in x])
    build = [[list(header)] for x in range(4)]
    protocol_header = ['Patient', 'Group', 'Session', 'Date', 'Researcher', 'Type', 'Name', 'Changes', 'Frequencies', 'Label', 'Duration',
                       'Name', 'Changes', 'Frequencies', 'Label', 'Duration', 'Notes']
    protocol = [list(protocol_header)]
    for single in process:
        line = [list('{} {} {} {}'.format(single.patient_id, single.user.group, single.session, single.date)[:-9].split(' '))
                for x in range(4)]
        for q in sorted([one for one in single.question], key=lambda x: x.question):
            for i, val in zip(range(0,4), (q.intensity, q.frequency, q.change, q.notes)):
                line[i].append(val)
        for i in range(4):
            build[i].append(line[i])
        append = False
        for protocol_line in single.protocol:
            if not append:
                protocol_to_add = [single.patient_id, single.user.group, single.session, str(single.date)[:-9],
                                   protocol_line.r_last_name, protocol_line.protocol_type,
                                   protocol_line.protocol_name_1 + '-' + protocol_line.protocol_name_2,
                                   protocol_line.changes, protocol_line.frequencies, protocol_line.label,
                                   protocol_line.duration, '','','','','',protocol_line.notes]
                protocol.append(protocol_to_add)
                if protocol_line.protocol_type == '2ch':
                    append = True
            else:
                second_line = [protocol_line.protocol_name_1 + '-' + protocol_line.protocol_name_2,
                                   protocol_line.changes, protocol_line.frequencies, protocol_line.label,
                                   protocol_line.duration]
                second_line.append(protocol[-1].pop())
                protocol[-1] = protocol[-1][:-5]
                protocol[-1].extend(second_line)
                append = False

    for key, value in zip(('intensity', 'frequency', 'change', 'notes'), range(0,4)):
        to_ret[key] = build[value]
    to_ret['protocol'] = protocol
    if patient_data:
        to_ret['patient data'] = get_patient_data(process[0].user)
    if intake_data:
        to_ret['intake data'] = get_intake_data(process[0].user)
    return to_ret


def get_patient_data(user):
    return [['group', user.group],
              ['patient_id', user.patient_id],
              ['sessions', user.sessions],
              ['initial_intake', user.initial_intake],
              ['date_of_birth', user.date_of_birth],
              ['guardian_names', user.guardian_names],
              ['custody', user.custody],
              ['gender', user.gender],
              ['address', user.address],
              ['phone', user.phone],
              ['email', user.email],
              ['handed', user.handed],
              ['diagnosis', user.diagnosis],
              ['reason_for_treatment', user.reason_for_treatment],
              ['current_medication', user.current_medication],
              ['previous_medication', user.previous_medication],
              ['referral', user.referral]
            ]


def get_intake_data(user):
    questions = [y for x in Intake.get_intake_questions() for y in x]
    i_data = []
    for q in user.intake:
        i_data.append([q.question, questions[int(q.question)-1], q.answer, q.details])
    return i_data


def get_forms(dates, initial, form_type, id):
    form_query = Form.query \
        .filter(Form.patient_id == id,
                Form.name == form_type)
    if form_query is None:
        return None
    if dates == 'all' or len(form_query.all()) <= int(dates):
        return form_query.from_self()\
            .order_by(Form.session) \
            .all()
    to_ret = form_query.from_self()\
        .order_by(desc(Form.session))\
        .limit(int(dates)) \
        .from_self() \
        .order_by(Form.session)
    if initial:
        process = [form_query.first()]
        process.extend(to_ret)
        return process
    return to_ret.all()
