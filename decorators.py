from flask import session, current_app, redirect, url_for, flash, abort
from functools import wraps
from app.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as TimedSerializer
from flask_login import current_user



def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            flash(u'Your session has expired.', 'error')
            return redirect(url_for('main.index'))
        s = TimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(session['token'])
        except:
            session.clear()
            flash(u'Your session has expired.', 'error')
            return redirect(url_for('main.index'))
        single_user = User.query\
            .filter(User.patient_id == data.get('auth'))\
            .first()
        if single_user is None:
            flash(u'Your session has expired.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs, single_user=single_user)
    return decorated_function

def master_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_master():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function