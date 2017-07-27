from flask import render_template, request, jsonify, session, flash, redirect, url_for, current_app
from . import main
from .forms import NewSessionForm, IdentifyAssessmentForm
from ..models import Form, Question, User
from .. import db
from decorators import token_required
from itsdangerous import TimedJSONWebSignatureSerializer as TimedSerializer
from sqlalchemy.sql.expression import desc, asc, func
from bleach import clean
from itertools import zip_longest
from datetime import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NewSessionForm(request.form)
    if request.method == 'POST':
        if form.validate():
            first_name = clean(form.first_name.data)
            last_name = clean(form.last_name.data)
            patient_id = clean(form.patient_id.data)
            user = User.query\
                .filter(User.patient_id == patient_id)\
                .first()
            if user is not None and user.decrypt_first_name() == first_name and \
                    user.decrypt_last_name() == last_name:
                s = TimedSerializer(current_app.config['SECRET_KEY'], 1800)
                session['token'] = s.dumps({'auth': clean(patient_id)})
                session['name'] = user.decrypt_first_name() + ' ' + user.decrypt_last_name()
                return redirect(url_for('main.begin'))
        flash(u'Please check entered data.', 'error')
        return redirect(url_for('main.index'))
    return render_template('main/index.html', form=form)


@main.route('/begin', methods=['GET', 'POST'])
@token_required
def begin(single_user):
    form = IdentifyAssessmentForm(request.form)
    if request.method == 'POST':
        if form.validate():
            single_assessment = Form.query.get(int(clean(form.assessment.data)))
            if single_assessment is None:
                flash(u'This form is not currently available', 'error')
                return redirect(url_for('main.begin'))
            else:
                session['form'] = single_assessment.id
                return redirect(url_for('main.form'))
        else:
            flash(u'Please check form entry', 'error')
            return redirect(url_for('main.begin'))
    else:
        assessments = Form.query \
            .filter(Form.patient_id == single_user.patient_id,
                    Form.section != None) \
            .order_by(desc(Form.date)) \
            .all()
        if len(assessments) == 0:
            session.clear()
            flash(u'You do not have any assessments to fill out at this time', 'error')
            return redirect(url_for('main.index'))
        to_display = [(a.id, datetime.strftime(a.date, '%b %d, %Y')) for a in assessments]
        return render_template('main/begin.html', assessments=to_display, form=form)


@main.route('/form')
@token_required
def form(single_user):
    if 'form' not in session:
        session.clear()
        flash(u'Your session has expired', 'error')
        return redirect(url_for('main.index'))
    current_form = Form.query.get(session['form'])
    if current_form is None:
        flash(u'There has been an error', 'error')
        return redirect(url_for('main.index'))
    section = current_form.section
    questions = Form.get_questions(current_form.name)
    if section >= len(questions):
        return redirect(url_for('main.finish'))
    buffer = sum([len(questions[s]) for s in range(0,section)])
    question_numbers = [i + buffer + 1 for i in range(0,len(questions[section]))]
    responses = Question.query\
        .filter(Question.form_id == current_form.id)\
        .filter(Question.question.in_(question_numbers))\
        .order_by(asc(Question.question))\
        .all()
    return render_template('main/form.html', questions=zip_longest(questions[section], responses),
                           complete=(section+1)*100//len(questions),
                           buffer=buffer,
                           responses=responses)


@main.route('/process', methods=['POST'])
@token_required
def process(single_user):
    data = request.get_json(force=True)
    current_form = Form.query.get(session['form'])
    if current_form is None:
        return jsonify({'code': '400'})
    for question in data:
        if data[question] is True:
            current_form.section += 1
        elif data[question] is False:
            current_form.section -= 1
            if current_form.section < 0:
                current_form.section = 0
        else:
            update_question = Question.query\
                .filter(Question.form_id == current_form.id,
                        Question.question == question)\
                .first()
            if data[question] == 'skip':
                if update_question is None:
                    question_to_add = Question(form_id=current_form.id, question=question,
                                               intensity=None,
                                               frequency=None,
                                               change=None,
                                               notes='')
                    db.session.add(question_to_add)
                else:
                    update_question.intensity = None
                    update_question.frequency = None
                    update_question.change = None
                    update_question.notes = ''
                    db.session.add(update_question)

            else:
                if update_question is None:
                    question_to_add = Question(form_id=current_form.id, question=question,
                                               intensity=clean(data[question]['i']),
                                               frequency=clean(data[question]['f']),
                                               change=clean(data[question]['c']),
                                               notes=clean(data[question]['n']))
                    db.session.add(question_to_add)
                else:
                    update_question.intensity = clean(data[question]['i'])
                    update_question.frequency = clean(data[question]['f'])
                    update_question.change = clean(data[question]['c'])
                    update_question.notes = clean(data[question]['n'].replace(',','-').replace(';','-'))
                    db.session.add(update_question)
    db.session.add(current_form)
    db.session.commit()
    return jsonify({'code': '201'})


@main.route('/finish')
@token_required
def finish(single_user):
    current_form = Form.query.get(session['form'])
    if current_form is None:
        return jsonify({'code': '400'})
    current_form.section = None
    db.session.add(current_form)
    db.session.add(single_user)
    db.session.commit()
    session.clear()
    return render_template('main/finish.html')