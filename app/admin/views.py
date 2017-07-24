from flask import render_template, request, flash, redirect, url_for, abort, current_app
from . import admin
from .forms import NewSessionForm, NewUserForm, NewResearcherForm, RemoveResearcherForm
from ..models import Form, Question, User, Researcher
from .. import db
from random import randint
from bleach import clean


@admin.route('/')
def index():
    return redirect(url_for('admin.user'))


@admin.route('/new_researcher', methods=['GET', 'POST'])
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
    return render_template('admin/new_researcher.html', form=form)


@admin.route('/remove_researcher', methods=['GET', 'POST'])
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
            elif r.role == 'ainat':
                flash(u'Ainat cannot be removed from this system', 'error')
            else:
                db.session.delete(r)
                db.session.commit()
                flash(u'{} has been removed from this system'.format(email), 'success')
            return redirect(url_for('admin.remove_researcher'))
        else:
            flash(u'Error on form inputs', 'error')
            return redirect(url_for('admin.remove_researcher'))
    return render_template('admin/remove_researcher.html', form=form)


@admin.route('/user', methods=['GET', 'POST'])
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

            to_add = User(first_name=clean_first, last_name=clean_last, patient_id = clean_id)
            db.session.add(to_add)
            db.session.commit()
            flash(u"This user has been added to database", 'success')
            return redirect(url_for('admin.user'))
        flash(u'Please recheck form', 'error')
        return redirect(url_for('admin.user'))
    return render_template('admin/user.html', form=form)


@admin.route('/new_session', methods=['GET', 'POST'])
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
                .filter(Form.user_id == user.id,
                        Form.date == clean_date,
                        Form.section == 0) \
                .first()
            if assessment is not None:
                flash(u'This patient already has a session scheduled for this day', 'error')
                return redirect(url_for('admin.new_session'))
            new_assessment = Form(user_id = user.id, date = clean_date, name=clean_form_type)
            db.session.add(new_assessment)
            db.session.commit()
            flash(u'This patient has a new session scheduled.', 'success')
            return redirect(url_for('admin.new_session'))
        else:
            flash(u'Please fill entire form', 'error')
            return redirect(url_for('admin.new_session'))
    return render_template('admin/new_session.html', form=form)


@admin.route('/display_form')
def display_form():
    # id = int(request.args.get('id'))
    id = 1
    form = Form.query.get(id)
    if form is None:
        abort(400)
    responses = form.question\
        .order_by(Question.id)\
        .all()
    questions = [ele for sub in Form.get_questions() for ele in sub]
    to_display = zip(questions, responses)
    return render_template('admin/display_form.html', to_display=to_display, id=id)


@admin.route('/compare_forms')
def compare_forms():
    id1 = 1
    id2 = 20
    form1 = Form.query.get(id1)
    form2 = Form.query.get(id2)
    if form1 is None or form2 is None:
        abort(400)
    responses1 = form1.question\
        .order_by(Question.id)\
        .all()
    responses2 = form2.question\
        .order_by(Question.id)\
        .all()
    questions = [ele for sub in Form.get_questions() for ele in sub]
    to_display = zip(questions, responses1, responses2)
    return render_template('admin/display_form.html', to_display=to_display, id=id)
