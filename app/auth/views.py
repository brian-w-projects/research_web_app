from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import RegisterForm, LoginForm, TokenForm
from ..models import Researcher
from .. import db
from bleach import clean


@auth.route('/token', methods=['GET', 'POST'])
def token():
    form = TokenForm(request.form)
    if request.method == 'POST':
        if form.validate():
            clean_token = clean(form.token.data)
            r = Researcher.query \
                .filter(Researcher.email == clean(form.email.data),
                        Researcher.token == clean_token) \
                .first()
            if r is None:
                flash(u'Please check form', 'error')
                return redirect(url_for('auth.token'))
            flash(u'Please complete registration', 'success')
            return redirect(url_for('auth.register', token=clean_token))
        else:
            flash(u'Please check form', 'error')
            return redirect(url_for('auth.token'))
    return render_template('auth/token.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if 'token' not in request.args or (request.referrer != url_for('auth.token', _external=True) and
                    request.referrer != url_for('auth.register', token=request.args.get('token'), _external=True)):
        abort(403)
    token = request.args.get('token')
    r = Researcher.query\
        .filter(Researcher.token == clean(token))\
        .first()
    if r is None:
        abort(403)
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate():
            r.password = clean(form.password.data)
            r.first_name = clean(form.first_name.data.strip().lower())
            r.last_name = clean(form.last_name.data.strip().lower())
            r.token = None
            db.session.add(r)
            db.session.commit()
            flash(u'You have successfully registered', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(u'Check form inputs', 'error')
            return redirect(url_for('admin.register', token=token))
    form.token.data = token
    form.email.data = r.email
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            check_user = Researcher.query\
                .filter(Researcher.email == clean(form.email.data),
                        Researcher.token == None)\
                .first()
            if check_user is None:
                flash(u'Invalid Information. Do you need to register?', 'error')
                return redirect(url_for('auth.login'))
            if check_user.verify_password(clean(form.password.data)):
                login_user(check_user)
                return redirect(request.args.get('next') or url_for('admin.index'))
            else:
                flash(u'Invalid Information', 'error')
                return redirect(url_for('auth.login'))
        else:
            flash(u'Invalid Information', 'error')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'Successfully logged out', 'success')
    return redirect(url_for('auth.login'))