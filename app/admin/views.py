from flask import render_template, request, flash, redirect, url_for
from . import admin
from .forms import NewSessionForm, NewUserForm, NewResearcherForm, RemoveResearcherForm, NewPasswordForm, PasswordResetForm
from ..models import Form, User, Researcher
from .. import db
from random import randint
from bleach import clean
from flask_login import login_required, current_user
from decorators import master_required


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
            while True:
                new_token = randint(10000, 99999)
                collision = Researcher.query \
                    .filter(Researcher.token == new_token) \
                    .first()
                if collision is None:
                    break
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
            user = User.query \
                .filter(User.patient_id == clean_id) \
                .first()
            if user is not None:
                flash(u'A patient with this ID has already been registered', 'error')
                return redirect(url_for('admin.user'))
            to_add = User(first_name=clean_first, last_name=clean_last, patient_id=clean_id)
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
            clean_first = clean(form.first.data).strip().lower()
            clean_last = clean(form.last.data).strip().lower()
            clean_date = clean(form.date.data)
            clean_form_type = clean(form.form_name.data)
            user = User.query \
                .filter(User.patient_id == clean_id) \
                .first()
            if user is None or user.decrypt_last_name() != clean_last or \
                    user.decrypt_first_name() != clean_first:
                flash(u'This user does not exist. Either add them to system or check data', 'error')
                return redirect(url_for('admin.new_session'))
            assessment = Form.query \
                .filter(Form.patient_id == user.patient_id,
                        Form.date == clean_date) \
                .first()
            if assessment is not None:
                flash(u'This patient already has a session scheduled for this day', 'error')
                return redirect(url_for('admin.new_session'))
            new_assessment = Form(patient_id=user.patient_id, date=clean_date, name=clean_form_type)
            db.session.add(new_assessment)
            db.session.commit()
            flash(u'This patient has a new session scheduled.', 'success')
            return redirect(url_for('admin.new_session'))
        else:
            flash(u'Please fill entire form', 'error')
            return redirect(url_for('admin.new_session'))
    return render_template('admin/new_session.html', form=form)


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
            flash(u'Please check enetered data', 'error')
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
                while True:
                    new_token = randint(10000, 99999)
                    collision = Researcher.query \
                        .filter(Researcher.token == new_token) \
                        .first()
                    if collision is None:
                        break
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
