from flask import render_template, request, flash, redirect, url_for, abort, current_app
from flask_login import current_user
from . import auth
from .forms import RegisterForm
from ..models import Form, Question, User, Researcher
from .. import db
from bleach import clean

# START WORKING HERE
@auth.route('/<int:token>', methods=['GET', 'POST'])
def register(token):
    r = Researcher.query\
        .filter(Researcher.token == token)\
        .first()
    if r is None:
        abort(404)
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate():
            r.password = clean(form.password.data)
            r.first_name = clean(form.first_name.data.strip().lower())
            r.last_name = clean(form.last_name.data.strip().lower())
            r.confirmed = True
            r.token = None
            db.session.add(r)
            db.session.commit()
        else:
            flash(u'Check form inputs', 'error')
            return redirect(url_for('register', token=token))
    form.token.data = token
    form.email.data = r.email
    return render_template('auth/register.html', form=form)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed \
            and not request.endpoint.startswith(('auth', 'main')) \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))