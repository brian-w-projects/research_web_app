from flask import render_template, request, jsonify, session, flash, redirect, url_for, current_app
from . import main
from .forms import TokenForm
from ..models import Form, Question, User
from .. import db
from decorators import token_required
from itsdangerous import TimedJSONWebSignatureSerializer as TimedSerializer
from sqlalchemy.sql.expression import desc, asc
from bleach import clean
from itertools import zip_longest


@main.route('/', methods=['GET', 'POST'])
def index():
    form = TokenForm(request.form)
    if request.method == 'POST':
        if form.validate():
            first_name = clean(form.first_name.data)
            last_name = clean(form.last_name.data)
            token = clean(form.token.data)
            user = User.query\
                .filter(User.token == token)\
                .first()
            if user is not None and user.decrypt_first_name() == first_name and \
                    user.decrypt_last_name() == last_name:
                current_form = user.form \
                    .order_by(desc(Form.timestamp)) \
                    .first()
                if current_form is None or current_form.section is None:
                    new_form = Form(user=user)
                    db.session.add(new_form)
                    db.session.commit()
                s = TimedSerializer(current_app.config['SECRET_KEY'], 1800)
                session['token'] = s.dumps({'auth': clean(form.token.data)})
                session['name'] = user.decrypt_first_name() + ' ' + user.decrypt_last_name()
                return redirect(url_for('main.form'))
        flash(u'Please check entered data.', 'error')
        return redirect(url_for('main.index'))
    return render_template('main/index.html', form=form)


@main.route('/form')
@token_required
def form(single_user):
    current_form = single_user.form\
        .order_by(desc(Form.timestamp))\
        .first()
    if current_form is None:
        flash(u'There has been an error with your token', 'error')
        return redirect(url_for('main.index'))
    section = current_form.section
    questions = Form.get_questions()
    if section >= len(questions):
        return redirect(url_for('main.finish'))
    buffer = sum([len(questions[s]) for s in range(0,section)])
    question_numbers = [i + buffer + 1 for i in range(0,len(questions[section]))]
    responses = Question.query\
        .filter(Question.form_id == current_form.id)\
        .filter(Question.question.in_(question_numbers))\
        .order_by(asc(Question.question))\
        .all()
    print('loading: ' + str(section))
    return render_template('main/form.html', questions=zip_longest(questions[section], responses),
                           complete=(section+1)*100//len(questions),
                           buffer=buffer,
                           responses=responses)


@main.route('/process', methods=['POST'])
@token_required
def process(single_user):
    data = request.get_json(force=True)
    current_form = single_user.form\
        .order_by(desc(Form.timestamp))\
        .first()
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
                    update_question.notes = clean(data[question]['n'])
                    db.session.add(update_question)
    db.session.add(current_form)
    db.session.commit()
    return jsonify({'code': '201'})


@main.route('/finish')
@token_required
def finish(single_user):
    current_form = single_user.form\
        .order_by(desc(Form.timestamp))\
        .first()
    if current_form is None:
        return jsonify({'code': '400'})
    current_form.section = None
    single_user.token = None
    db.session.add(current_form)
    db.session.add(single_user)
    db.session.commit()
    session.clear()
    return render_template('main/finish.html')