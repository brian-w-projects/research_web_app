from . import db
from datetime import datetime
from sqlalchemy.orm import backref
from flask import current_app
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as TimedSerializer
from . import login_manager
from flask_login import UserMixin

class Form(db.Model):
    __tablename__ = 'form'
    id = db.Column(db.INTEGER, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    section = db.Column(db.INTEGER, default=0, nullable=True)

    user = db.relationship('User', backref=backref('form', lazy='dynamic'))

    @staticmethod
    def get_questions():
        # questions = [['Difficulty paying attention, focusing or concentrating',
        #                        'Spacey, foggy'],
        #                        ['On guard, watchful, hypervigilant',
        #                        'Impulsive, acts without thinking',
        #                        'Not insightful, unobservant, inattentive'],
        #                        ['Restless, unable to sit still, fidgety',
        #                        'Racing thoughts']
        #                        ]

        # questions = [['1', '2'], ['3', '4', '5'], ['6', '7']]

        questions = [['Difficulty paying attention, focusing or concentrating',
                      'Spacey, foggy',
                      'On guard, watchful, hypervigilant',
                      'Impulsive, acts without thinking',
                      'Not insightful, unobservant, inattentive',
                      'Restless, unable to sit still, fidgety',
                      'Racing thoughts'],
                     ['Anxious, nervous, worried',
                      'Panic attacks',
                      'Sad',
                      'Sensitive, cries easily/often',
                      'Irritable, agitated or easily provoked',
                      'Unable to relax',
                      'Rage, aggression, tantrums, destructiveness',
                      'Withdrawn, shut-down, numb'],
                     ['Difficulty falling asleep',
                      'Difficulty staying asleep',
                      'Nightmares',
                      'Feels tired and fatigued after sleeping'],
                     ['Trouble getting along with peers or fitting in',
                      'Trouble engaging in activities',
                      'Trouble making and/or maintaining eye contact',
                      'Not playful',
                      'Not cooperative'],
                     ['Low energy, lack of motivation',
                      'High energy, seeks stimulation, tireless',
                      'Talks too fast/much/loud/high pitched',
                      'Talks to slow/soft or does not talk enough'],
                     ['Stomachaches',
                      'Headaches',
                      'Muscle tension',
                      'Constipation or diarrhea',
                      'Dizziness',
                      'Grinds or clenches teeth',
                      'Change in appetite (loss or gain)',
                      'Hands or legs shake, tremors',
                      'Hypersensitivity to light, touch and sounds',
                      'Lack of responsiveness to touch, pain and loud sounds',
                      'Tics',
                      'Skin crawling sensations',
                      'Bed Wetting']
                     ]
        return questions

    @staticmethod
    def generate_forms(count):
        from random import seed, randint, choice
        import forgery_py
        from datetime import timedelta

        print('Generating Forms')
        seed()
        user_count = User.query.count()
        form_date = datetime.utcnow() - timedelta(days=365)
        for i in range(count):
            if i%100 == 0:
                print('{} of {}'.format(str(i), str(count)))
            u = User.query\
                .offset(randint(0, user_count-1))\
                .first()
            f = Form(user_id=u.id, section=None,
                     timestamp=form_date)
            db.session.add(f)
            for j in range(1,8):
                q = Question(form=f, question=j,
                             intensity=randint(0,4), frequency=randint(0,4),
                             change=choice('BSW'),
                             notes=forgery_py.lorem_ipsum.sentences(randint(1,3)) if randint(1,5) == 2 else '')
                db.session.add(q)
            db.session.commit()
            form_date = form_date + timedelta(days=randint(1, 5))
            if form_date > datetime.utcnow():
                break
        print('{} of {}'.format(str(count), str(count)))

    def __repr__(self):
        return "Form(user_id={self.user_id})".format(self=self)

    def __str__(self):
        return self.__repr__()


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.INTEGER, primary_key=True)
    form_id = db.Column(db.INTEGER, db.ForeignKey('form.id'))
    question = db.Column(db.INTEGER)
    intensity = db.Column(db.INTEGER, nullable=True)
    frequency = db.Column(db.INTEGER, nullable=True)
    change = db.Column(db.String, nullable=True)
    notes = db.Column(db.TEXT)

    form = db.relationship('Form', backref=backref('question', lazy='dynamic'))

    def __repr__(self):
        return "Question(form_id={self.form_id}, question={self.question}, " \
               "intensity={self.intensity}, frequency={self.frequency}, change={self.change}, " \
               "notes={self.notes})".format(self=self)

    def __str__(self):
        return self.__repr__()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.INTEGER, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    token = db.Column(db.INTEGER, nullable=True)

    @staticmethod
    def generate_users(count):
        import forgery_py

        print('Generating users')
        for i in range(count):
            if i%100 == 0:
                print('{} of {}'.format(str(i), str(count)))
            first = forgery_py.name.first_name().strip().lower()
            last = forgery_py.name.last_name().strip().lower()

            add = True

            for user in User.query.all():
                if user.first_name == first and \
                                user.last_name == last:
                    add = False

            if add is False:
                continue

            u = User(first_name=first, last_name=last)
            db.session.add(u)
            db.session.commit()
        print('{} of {}'.format(str(count), str(count)))

    def __repr__(self):
        return "User(first_name={self.first_name_encrypt}, last_name={self.last_name_encrypt})".format(self=self)

    def __str__(self):
        return self.__repr__()


class Researcher(UserMixin, db.Model):
    __tablename__ = 'researcher'
    id = db.Column(db.INTEGER, primary_key=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    role = db.Column(db.String, default='admin')
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    confirmed = db.Column(db.BOOLEAN, default=False)
    token = db.Column(db.INTEGER, nullable=True)

    @property
    def password(self):
        raise AttributeError('password is hashed')

    @password.setter
    def password(self, p):
        self.password_hash = generate_password_hash(p)

    def verify_password(self, p):
        return check_password_hash(self.password_hash, p)

    def generate_confirmation_token(self, expiration=3600):
        s = TimedSerializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = TimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.commit(self)
        db.session.commit()
        return True

    def is_master(self):
        return self.role == 'master'

    def __repr__(self):
        return "Researcher(email={self.email}, first_name={self.first_name}, last_name={self.last_name}".format(self=self)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
