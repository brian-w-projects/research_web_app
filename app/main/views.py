from flask import render_template, request, jsonify, session, flash, redirect, url_for, current_app
from . import main
from .forms import NewSessionForm, IdentifyAssessmentForm, GeneralIntake
from ..models import Form, Question, User, Intake, Cortical, Arousal, Major
from .. import db
from decorators import token_required
from itsdangerous import TimedJSONWebSignatureSerializer as TimedSerializer
from sqlalchemy.sql.expression import desc, asc
from bleach import clean
from itertools import zip_longest
from datetime import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NewSessionForm(request.form)
    if request.method == 'POST':
        if form.validate():
            first_name = clean(form.first_name.data).strip().lower()
            last_name = clean(form.last_name.data).strip().lower()
            patient_id = clean(form.patient_id.data)
            user = User.query\
                .filter(User.patient_id == patient_id)\
                .first()
            if user is not None and user.verify_name(first_name, last_name):
                s = TimedSerializer(current_app.config['SECRET_KEY'], 1800)
                session['token'] = s.dumps({'auth': clean(patient_id)})
                session['name'] = first_name + ' ' + last_name
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
                if single_assessment.name == 'A':
                    return redirect(url_for('main.form'))
                elif single_assessment.name == 'B':
                    return redirect(url_for('main.cortical'))
                elif single_assessment.name == 'C':
                    return redirect(url_for('main.arousal'))
                else:
                    return redirect(url_for('main.major'))
        else:
            flash(u'Please check form entry', 'error')
            return redirect(url_for('main.begin'))
    else:
        assessments = Form.query \
            .filter(Form.patient_id == single_user.patient_id,
                    Form.section != None) \
            .order_by(desc(Form.date)) \
            .all()
        if len(assessments) == 0 and single_user.intake_page is None:
            session.clear()
            flash(u'You do not have any assessments to fill out at this time', 'error')
            return redirect(url_for('main.index'))
        form_names = {'A': 'Session Self Report', 'B': 'Symptoms and Cortical Networks',
                      'C': 'Arousal Assessment', 'D': 'Major Self Report'}
        to_display = [(a.id, datetime.strftime(a.date, '%b %d, %Y')+' -- '+form_names[a.name]) for a in assessments]
        return render_template('main/begin.html', assessments=to_display, form=form,
                               intake=single_user.intake_page is not None)


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
    questions = current_form.get_questions()
    if section >= len(questions):
        return redirect(url_for('main.finish'))
    buffer = sum([len(questions[s]) for s in range(0,section)])
    question_numbers = [i + buffer + 1 for i in range(0,len(questions[section]))]
    responses = Question.query\
        .filter(Question.form_id == current_form.id)\
        .filter(Question.question.in_(question_numbers))\
        .order_by(asc(Question.question))\
        .all()
    title = current_form.get_title()
    return render_template('main/form.html', questions=zip_longest(questions[section], responses),
                           complete=(section+1)*100//len(questions),
                           buffer=buffer,
                           responses=responses,
                           title=title)


@main.route('/process', methods=['POST'])
@token_required
def process(single_user):
    data = request.get_json(force=True)
    if 'form' not in session:
        session.clear()
        flash(u'Your session has expired', 'error')
        return redirect(url_for('main.index'))
    current_form = Form.query.get(session['form'])
    if current_form is None:
        return jsonify({'code': '400'})
    for question in data:
        if data[question] is True:
            current_form.section += 1
        elif data[question] is False:
            current_form.section -= 1
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
    if 'form' not in session:
        session.clear()
        flash(u'There has been an error', 'error')
        return redirect(url_for('main.index'))
    current_form = Form.query.get(session['form'])
    if current_form is None:
        return jsonify({'code': '400'})
    current_form.section = None
    db.session.add(current_form)
    db.session.add(single_user)
    db.session.commit()
    session.clear()
    return render_template('main/finish.html')


@main.route('/general_information', methods=['GET', 'POST'])
@token_required
def general_information(single_user):
    if single_user.intake_page is None:
        flash(u'You have already filled this form out', 'error')
        return redirect(url_for('main.index'))
    elif single_user.intake_page != -1:
        return redirect(url_for('main.intake'))
    form = GeneralIntake(obj=single_user)
    if request.method == 'POST':
        del form.patient_id
        form.populate_obj(single_user)
        single_user.intake_page = 0
        db.session.add(single_user)
        db.session.commit()
        return redirect(url_for('main.intake'))
    return render_template('main/general_information.html', form=form)


@main.route('/intake', methods=['GET', 'POST'])
@token_required
def intake(single_user):
    page = single_user.intake_page
    questions = Intake.get_intake_questions()
    buffer = sum([len(questions[s]) for s in range(0, page)])
    if request.method == 'POST':
        for i in range(1,len(questions[page])+1):
            to_add = Intake(patient_id=single_user.patient_id, question=i+buffer,
                            answer=request.form[str((i+buffer))+ " a"],
                            details=request.form[(str(i+buffer))+ " n"])
            db.session.add(to_add)
            db.session.commit()
        single_user.intake_page += 1
        db.session.add(single_user)
        db.session.commit()
        page += 1
        buffer = sum([len(questions[s]) for s in range(0, page)])
    if single_user.intake_page >= len(questions):
        single_user.intake_page = None
        db.session.add(single_user)
        db.session.commit()
        return redirect(url_for('main.intake_finish'))
    return render_template('main/intake_form.html', questions=questions[page],
                           complete=(page+1)*100//len(questions),
                           buffer=buffer)


@main.route('/intake_finish')
@token_required
def intake_finish(single_user):
    single_user.intake_page = None
    db.session.add(single_user)
    db.session.commit()
    session.clear()
    return render_template('main/intake_finish.html')


@main.route('/cortical', methods=['GET', 'POST'])
@token_required
def cortical(single_user):
    if 'form' not in session:
        session.clear()
        flash(u'Your session has expired', 'error')
        return redirect(url_for('main.index'))
    current_form = Form.query.get(session['form'])
    if current_form is None:
        flash(u'There has been an error', 'error')
        return redirect(url_for('main.index'))
    section = current_form.section
    questions = current_form.get_questions()
    if section >= len(questions):
        return redirect(url_for('main.finish'))
    buffer = sum([len(questions[s]) for s in range(0,section)])
    title = current_form.get_title()
    if request.method == 'POST':
        for i in range(1, len(questions[current_form.section]) + 1):
            to_add = Cortical(form_id=current_form.id, question=i+buffer,
                              response=request.form[str((i+buffer))+' '] if str((i+buffer))+' ' in request.form else '')
            db.session.add(to_add)
            db.session.commit()
        current_form.section += 1
        db.session.add(current_form)
        db.session.commit()
        return redirect(url_for('main.cortical'))
    return render_template('main/cortical.html', questions=questions[section],
                           complete=(section+1)*100//len(questions),
                           buffer=buffer,
                           title=title)


@main.route('/arousal', methods=['GET', 'POST'])
@token_required
def arousal(single_user):
    if 'form' not in session:
        session.clear()
        flash(u'Your session has expired', 'error')
        return redirect(url_for('main.index'))
    current_form = Form.query.get(session['form'])
    if current_form is None:
        flash(u'There has been an error', 'error')
        return redirect(url_for('main.index'))
    section = current_form.section
    questions = current_form.get_questions()
    if section >= len(questions):
        return redirect(url_for('main.finish'))
    buffer = sum([len(questions[s]) for s in range(0,section)])
    title = current_form.get_title()
    if request.method == 'POST':
        for i in range(1, len(questions[current_form.section]) + 1):
            to_add = Arousal(form_id=current_form.id, question=i+buffer,
                              response=request.form[str((i+buffer))+' '] if str((i+buffer))+' ' in request.form else '')
            db.session.add(to_add)
            db.session.commit()
            print(to_add)
        current_form.section += 1
        db.session.add(current_form)
        db.session.commit()
        return redirect(url_for('main.arousal'))
    return render_template('main/arousal.html', questions=questions[section],
                           complete=(section+1)*100//len(questions),
                           buffer=buffer,
                           title=title)


@main.route('/major', methods=['GET', 'POST'])
@token_required
def major(single_user):
    if 'form' not in session:
        session.clear()
        flash(u'Your session has expired', 'error')
        return redirect(url_for('main.index'))
    current_form = Form.query.get(session['form'])
    if current_form is None:
        flash(u'There has been an error', 'error')
        return redirect(url_for('main.index'))
    section = current_form.section
    questions = current_form.get_questions()
    if section >= len(questions):
        return redirect(url_for('main.finish'))
    buffer = sum([len(questions[s]) for s in range(0,section)])
    title = current_form.get_title()
    if request.method == 'POST':
        for i in range(1, len(questions[current_form.section]) + 1):
            to_add = Major(form_id=current_form.id, question=i+buffer,
                  response=request.form[str((i+buffer))+' '] if str((i+buffer))+' ' in request.form else '')
            db.session.add(to_add)
            db.session.commit()
            print(to_add)
        current_form.section += 1
        db.session.add(current_form)
        db.session.commit()
        return redirect(url_for('main.major'))
    return render_template('main/major.html', questions=questions[section],
                           complete=(section+1)*100//len(questions),
                           buffer=buffer,
                           title=title)