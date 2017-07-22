from flask import render_template, request, flash, redirect, url_for, abort, current_app
from . import admin
from .forms import NewTokenForm, NewUserForm, NewResearcherForm, RemoveResearcherForm
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
            for single_user in User.query.all():
                if single_user.first_name == clean_first and \
                        single_user.last_name == clean_last:
                    flash(u"This user already exists in database", 'error')
                    return redirect(url_for('admin.user'))
            to_add = User(first_name=clean_first, last_name=clean_last)
            db.session.add(to_add)
            db.session.commit()
            flash(u"This user has been added to database", 'success')
            return redirect(url_for('admin.user'))
        flash(u'Please recheck form', 'error')
        return redirect(url_for('admin.user'))
    return render_template('admin/user.html', form=form)


@admin.route('/token', methods=['GET', 'POST'])
def token():
    form = NewTokenForm(request.form)
    if request.method == 'POST':
        if form.validate():
            clean_first = clean(form.first.data).strip().lower()
            clean_last = clean(form.last.data).strip().lower()
            for single_user in User.query.all():
                if single_user.first_name == clean_first and \
                                single_user.last_name == clean_last:
                    if single_user.token is None:
                        while True:
                            new_token = randint(10000, 99999)
                            collision = User.query\
                                .filter(User.token == new_token)\
                                .first()
                            if collision is None:
                                break
                        single_user.token = new_token
                        db.session.add(single_user)
                        db.session.commit()
                        flash(u"This user's token is: {}".format(new_token), 'success')
                    else:
                        flash(u"This user already has a token: {}".format(single_user.token), 'success')
                    return redirect(url_for('admin.token'))
            flash(u'This user is not in the system. Please check spelling or add user first.', 'error')
            return redirect(url_for('admin.token'))
        flash(u'Please fill out entire form', 'error')
        return redirect(url_for('admin.token'))
    return render_template('admin/user.html', form=form)


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
