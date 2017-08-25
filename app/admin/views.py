from flask import render_template, request, flash, redirect, url_for, jsonify, session
from . import admin
from .forms import NewSessionForm, NewUserForm, NewResearcherForm, RemoveResearcherForm, \
    NewPasswordForm, PasswordResetForm, ProtocolForm, UpdatePatientForm, GeneralIntakeForm
from ..models import Form, User, Researcher, Protocol
from .. import db
from random import randint
from bleach import clean
from flask_login import login_required, current_user
from decorators import master_required
from sqlalchemy.sql.expression import or_, desc


@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@admin.route('/new_researcher', methods=['GET', 'POST'])
@login_required
@master_required
def new_researcher():
    form = NewResearcherForm(request.form)
    if request.method == 'POST':
        if form.validate():
            email = clean(form.email.data)
            check = Researcher.query \
                .filter(Researcher.email == email)\
                .first()
            if check is not None:
                if check.token is None:
                    flash(u'This user is already registered', 'error')
                else:
                    flash(u'This email address is already registered. Token is {}'.format(str(check.token)), 'error')
                return redirect(url_for('admin.new_researcher'))
            new_token = Researcher.generate_token()
            r = Researcher(email=email, token=new_token)
            db.session.add(r)
            db.session.commit()
            flash(u'Token is : {}'.format(str(new_token)), 'success')
            return redirect(url_for('admin.new_researcher'))
        else:
            flash(u'Error on form inputs', 'error')
            return redirect(url_for('admin.new_researcher'))
    display = Researcher.query \
        .filter(Researcher.token != None) \
        .all()
    return render_template('admin/new_researcher.html', form=form, display=display)


@admin.route('/remove_researcher', methods=['GET', 'POST'])
@login_required
@master_required
def remove_researcher():
    form = RemoveResearcherForm(request.form)
    if request.method == 'POST':
        if form.validate():
            email = clean(form.email.data)
            r = Researcher.query\
                .filter(Researcher.email == email)\
                .first()
            if r is None:
                flash(u'This email is not registered in this system', 'error')
            elif r.is_master():
                flash(u'This user cannot be removed from this system', 'error')
            else:
                db.session.delete(r)
                db.session.commit()
                flash(u'{} has been removed from this system'.format(email), 'success')
            return redirect(url_for('admin.remove_researcher'))
        else:
            flash(u'Error on form inputs', 'error')
            return redirect(url_for('admin.remove_researcher'))
    display = Researcher.query \
        .order_by(Researcher.last_name) \
        .all()
    return render_template('admin/remove_researcher.html', form=form, display=display)


@admin.route('/new_patient', methods=['GET', 'POST'])
@login_required
def user():
    form = NewUserForm(request.form)
    if request.method == 'POST':
        if form.validate():
            clean_first = clean(form.first.data).strip().lower()
            clean_last = clean(form.last.data).strip().lower()
            clean_id = clean(form.patient_id.data)
            clean_dob = clean(form.dob.data)
            user = User.query \
                .filter(User.patient_id == clean_id) \
                .first()
            if user is not None:
                flash(u'A patient with this ID has already been registered', 'error')
                return redirect(url_for('admin.user'))
            to_add = User(first_name=clean_first, last_name=clean_last, patient_id=clean_id,
                          group=form.group.data, date_of_birth=clean_dob)
            to_add.create_folder()
            db.session.add(to_add)
            db.session.commit()
            flash(u"This user has been added to database", 'success')
            return redirect(url_for('admin.user'))
        flash(u'Please recheck form', 'error')
        return redirect(url_for('admin.user'))
    return render_template('admin/user.html', form=form)


@admin.route('/new_session', methods=['GET', 'POST'])
@login_required
def new_session():
    form = NewSessionForm(request.form)
    if request.method == 'POST':
        if form.validate():
            clean_id = clean(form.patient_id.data)
            clean_date = clean(form.date.data)
            clean_form_type = clean(form.form_name.data)
            user = User.query \
                .filter(User.patient_id == clean_id) \
                .first()
            if user is None:
                flash(u'This user does not exist. Either add them to system or check data', 'error')
                return redirect(url_for('admin.new_session'))
            assessment = Form.query \
                .filter(Form.patient_id == user.patient_id,
                        Form.date == clean_date,
                        Form.name == clean_form_type) \
                .first()
            if assessment is not None:
                flash(u'This patient already has a session scheduled for this day', 'error')
                return redirect(url_for('admin.new_session'))
            new_assessment = Form(patient_id=user.patient_id, date=clean_date, name=clean_form_type,
                                  session=user.sessions+1)
            user.sessions += 1
            db.session.add(new_assessment)
            db.session.add(user)
            db.session.commit()
            flash(u'This patient has a new session scheduled.', 'success')
            return redirect(url_for('admin.new_session'))
        else:
            flash(u'Please fill entire form', 'error')
            return redirect(url_for('admin.new_session'))
    raw = Form.query \
        .filter(Form.section != None) \
        .order_by(Form.patient_id, Form.date) \
        .all()
    form_names = {'A': 'Session Self Report', 'B': 'Symptoms and Cortical Networks',
                 'C': 'Arousal Assessment', 'D': 'Major Self Report'}
    sessions = [(f.patient_id, str(f.date)[0:-9], f.id, form_names[f.name]) for f in raw]
    return render_template('admin/new_session.html', form=form, sessions=sessions)


@admin.route('/delete_session', methods=['POST'])
@login_required
def delete_session():
    for ele in request.form:
        if ele not in ('csrf_token', 'submit'):
            f = Form.query.get(ele)
            db.session.delete(f)
    db.session.commit()
    flash(u'Sessions Successfully Delete', 'success')
    return redirect(url_for('admin.new_session'))


@admin.route('/update_intake', methods=['GET', 'POST'])
@login_required
def update_intake():
    if request.method == 'POST':
        if UpdatePatientForm(request.form).validate():
            form = UpdatePatientForm(request.form)
            clean_id = clean(form.patient_id.data)
            u = User.query \
                .filter(User.patient_id == clean_id) \
                .first()
            if u is not None:
                session['id_to_mod'] = u.patient_id
                return redirect(url_for('admin.update_general_intake'))
            else:
                flash(u'This patient does not exist', 'error')
                return redirect(url_for('admin.update_intake'))
        else:
            flash(u'Please check entered data', 'error')
            return redirect(url_for('admin.update_intake'))
    return render_template('admin/update_intake.html', form=UpdatePatientForm())


@admin.route('/update_general_intake', methods=['GET', 'POST'])
@login_required
def update_general_intake():
    if 'id_to_mod' not in session or session['id_to_mod'] is None:
        return redirect(url_for('admin.update_intake'))
    u = User.query \
        .filter(User.patient_id == session['id_to_mod']) \
        .first()
    form = GeneralIntakeForm(obj=u)
    if request.method == 'POST':
        del form.patient_id
        form.populate_obj(u)
        db.session.add(u)
        db.session.commit()
        flash(u'Patient intake information successfully updated', 'success')
        session['id_to_mod'] = None
        return redirect(url_for('admin.update_intake'))
    return render_template('admin/update_general_intake.html', form=form)


@admin.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = NewPasswordForm(request.form)
    if request.method == 'POST':
        if form.validate():
            clean_pw = clean(form.current_password.data)
            if current_user.verify_password(clean_pw) and clean(form.new_password.data) == form.new_password.data:
                current_user.password = form.new_password.data
                db.session.add(current_user)
                db.session.commit()
                flash(u'Password has been updated', 'success')
                return redirect(url_for('admin.update_password'))
            else:
                flash(u'Please check entered data', 'error')
                return redirect(url_for('admin.update_password'))
        else:
            flash(u'Please check entered data', 'error')
            return redirect(url_for('admin.update_password'))
    return render_template('admin/update_password.html', form=form)


@admin.route('/reset_password', methods=['GET', 'POST'])
@master_required
def reset_password():
    form = PasswordResetForm(request.form)
    if request.method == 'POST':
        if form.validate():
            clean_email = clean(form.email.data)
            r = Researcher.query \
                .filter(Researcher.email == clean_email) \
                .first()
            if r is None:
                flash(u'This user is not registered', 'error')
                return redirect(url_for('admin.reset_password'))
            elif r.token is not None:
                flash(u'This researcher already has a token for registration', 'error')
                return redirect(url_for('admin.reset_password'))
            elif r.is_master():
                flash(u'Master users may not reset their password to prevent lockout', 'error')
                return redirect(url_for('admin.reset_password'))
            else:
                new_token = Researcher.generate_token()
                r.token = new_token
                r.password = ''
                db.session.add(r)
                db.session.commit()
                flash(u'Researcher may register with token {}'.format(str(new_token)), 'success')
                return redirect(url_for('admin.reset_password'))
        else:
            flash(u'Please check entered data', 'error')
            return redirect(url_for('admin.reset_password'))
    display = Researcher.query \
        .filter(Researcher.token != None) \
        .all()
    return render_template('admin/reset_password.html', form=form, display=display)


@admin.route('/protocol', methods=['GET', 'POST'])
@login_required
def protocol():
    form = ProtocolForm(request.form)
    if request.method == 'POST':
        if form.validate():
            last_protocol = []
            if Protocol.query.filter(Protocol.patient_id == form.patient_id.data).first() is not None:
                last_form_id = Protocol.query \
                    .filter(Protocol.patient_id == form.patient_id.data) \
                    .order_by(desc(Protocol.form_id)) \
                    .first().form_id
                last_protocol = sorted(Protocol.query \
                    .filter(Protocol.patient_id == form.patient_id.data,
                            Protocol.form_id == int(last_form_id)) \
                    .order_by(desc(Protocol.form_id)) \
                    .all(), key=lambda x: x.row)
            return render_template('admin/protocol.html', patient_id=clean(form.patient_id.data),
                                                           form_id=clean(form.form_id.data),
                                                            last=last_protocol)
        else:
            flash(u'Please check form entries', 'error')
            return redirect(url_for('admin.protocol'))
    return render_template('admin/protocol_init.html', form=form)


@admin.route('/init_ajax', methods=['POST'])
@login_required
def init_ajax():
    id = request.get_json(force=True)
    to_ret = {}
    sessions = Form.query \
        .filter(Form.patient_id == id['id']) \
        .all()
    for ele in sessions:
        if ele.protocol.first() is None:
            to_ret[str(ele.id)] = (ele.id, str(ele.date)[:10])
    if len(to_ret) == 0:
        return jsonify({'code': '400'})
    else:
        to_ret['code'] = '201'
        return jsonify(to_ret)


@admin.route('/protocol_ajax', methods=['POST'])
@login_required
def protocol_ajax():
    data = request.get_json(force=True)
    patient_id = data[0]['value']
    form_id = data[1]['value']
    notes = data[-1]['value']
    if Protocol.query.filter(Protocol.patient_id == patient_id).first() is not None:
        last_form_id = Protocol.query \
            .filter(Protocol.patient_id == patient_id) \
            .order_by(desc(Protocol.form_id)) \
            .first().form_id
        last_protocols = [x.frequencies for x in Protocol.query \
            .filter(Protocol.patient_id == patient_id,
                    Protocol.form_id == last_form_id) \
            .order_by(Protocol.row).all()]
    else:
        last_protocols = []
    for i in range(2,len(data)-1,7):
        if data[i]['value'] != '':
            new_protocol = Protocol(patient_id=patient_id, row=int(data[i]['name'][0]),
                    r_last_name = current_user.last_name, number=data[i]['value'],
                    protocol_type=data[i+1]['value'],
                    site_1=data[i+2]['value'], site_2=data[i+3]['value'],
                    frequencies=data[i+4]['value'], label=data[i+5]['value'],
                    duration=data[i+6]['value'], game='filler', notes=notes if i == 2 else '',
                    form_id=form_id)
            if len(last_protocols) > 0:
                new_protocol.changes = False if last_protocols[0] == data[i+3]['value'] else True
                del last_protocols[0]
            db.session.add(new_protocol)
            db.session.commit()
    flash(u'Data successfully saved', 'success')
    return jsonify({'code': '201'})
