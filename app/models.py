from . import db
from datetime import datetime
from sqlalchemy.orm import backref
from flask import current_app
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as TimedSerializer
from . import login_manager
from flask_login import UserMixin
from sqlalchemy.sql.expression import or_, desc


class Form(db.Model):
    __tablename__ = 'form'
    id = db.Column(db.INTEGER, primary_key=True)
    session = db.Column(db.INTEGER, index=True)
    name = db.Column(db.String)
    date = db.Column(db.DateTime, index=True)
    patient_id = db.Column(db.String, db.ForeignKey('user.patient_id'))
    section = db.Column(db.INTEGER, default=0, nullable=True)

    user = db.relationship('User', backref=backref('form', lazy='dynamic'))

    @staticmethod
    def get_questions(name):

        return {'A': [['Difficulty paying attention, focusing or concentrating',
                       'Spacey, fogey',
                       'On guard, watchful, hypervigilant',
                       'Impulsive, acts without thinking',
                       'Insightful, observant, attentive',
                       'Restless, unable to sit still, fidgety',
                       'Racing thoughts',
                       'Flexible, tolerates changes'],
                      ['Anxious, nervous, worried',
                       'Panic attacks',
                       'Sad',
                       'Sensitive, cries easily/often',
                       'Irritable, agitated, or easily provoked',
                       'Able to relax',
                       'Rage, aggression, tantrums, destructiveness',
                       'Withdrawn, shut-down, numb'],
                      ['Falls asleep easily',
                       'Stays asleep',
                       'Nightmares',
                       'Feels tired and fatigued after sleeping'],
                      ['Gets along with peers, fits in',
                       'Engages in activities',
                       'Able to make and or maintain eye contact',
                       'Playful',
                       'Cooperative'],
                      ['Low energy, lack of motivation',
                       'High energy, seeks stimulation, tireless',
                       'Talks too fast much loud high pitched',
                       'Talks too slow soft or does not talk enough'],
                      ['Stomachaches',
                       'Headaches',
                       'Muscle tension',
                       'Constipation or diarrhea',
                       'Dizziness',
                       'Grinds or clenches teeth',
                       'Change in appetite',
                       'Hands or legs shake, tremors',
                       'Hypersensitivity to light, touch and sounds',
                       'Lack of responsiveness to touch, pain and loud sounds',
                       'Tics',
                       'Skin crawling sensations',
                       'Bed Wetting']],
                'B': [['B1', 'B2', 'B3', 'B4', 'B5']],
                'C': [['C1', 'C2', 'C3'], ['C4']]}.get(name)

    @staticmethod
    def generate_forms(count):
        from random import seed, randint, choice
        import forgery_py
        from datetime import timedelta

        print('Generating Forms')
        seed()
        user_count = User.query.count()
        form_date = datetime.utcnow() - timedelta(days=3650)
        for i in range(count):
            if i%100 == 0:
                print('{} of {}'.format(str(i), str(count)))
            u = User.query\
                .offset(randint(0, user_count-1))\
                .first()
            try:
                s = Form.query\
                    .filter(Form.patient_id == u.patient_id)\
                    .order_by(desc(Form.session))\
                    .first().session+1
            except:
                s = 1
            name = choice(['A', 'B', 'C'])
            f = Form(patient_id=u.patient_id,
                     date=form_date, name=name, session=s)
            u.session += 1
            db.session.add(f)
            db.session.add(u)
            for j in range(1,len([y for x in Form.get_questions(name) for y in x])+1):
                q = Question(form=f, question=j,
                             intensity=randint(0,4), frequency=randint(0,4),
                             change=randint(0,2),
                             notes=forgery_py.lorem_ipsum.sentences(randint(1,3)).replace(',','-').replace(';','-') if randint(1,5) == 2 else '')
                db.session.add(q)
            db.session.commit()
            form_date = form_date + timedelta(days=randint(1, 5))
            if form_date > datetime.utcnow():
                break
        print('{} of {}'.format(str(count), str(count)))

    def __repr__(self):
        return "Form(id={self.id}, session={self.session}, patient_id={self.patient_id}, " \
               "date={self.date}, section={self.section}, name={self.name})".format(self=self)

    def __str__(self):
        return self.__repr__()


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.INTEGER, primary_key=True)
    form_id = db.Column(db.INTEGER, db.ForeignKey('form.id'))
    question = db.Column(db.INTEGER)
    intensity = db.Column(db.INTEGER, nullable=True)
    frequency = db.Column(db.INTEGER, nullable=True)
    change = db.Column(db.INTEGER, nullable=True)
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
    group = db.Column(db.String, default='0')
    patient_id = db.Column(db.String, index=True, unique=True)
    first_name_hash = db.Column(db.String)
    last_name_hash = db.Column(db.String)
    sessions = db.Column(db.INTEGER, default=0)

    @property
    def first_name(self):
        raise AttributeError('first name is hashed')

    @first_name.setter
    def first_name(self, p):
        self.first_name_hash = generate_password_hash(p)

    @property
    def last_name(self):
        raise AttributeError('last name is hashed')

    @last_name.setter
    def last_name(self, p):
        self.last_name_hash = generate_password_hash(p)

    def verify_name(self, f, l):
        return check_password_hash(self.first_name_hash, f) and check_password_hash(self.last_name_hash, l)

    @staticmethod
    def generate_users(count):
        import forgery_py
        from random import randint

        print('Generating users')
        for i in range(count):
            if i%100 == 0:
                print('{} of {}'.format(str(i), str(count)))
            first = forgery_py.name.first_name().strip().lower()
            last = forgery_py.name.last_name().strip().lower()
            patient_id = str(randint(1, 10000))
            while True:
                u = User.query.filter(User.patient_id == patient_id).first()
                if u is None:
                    break
                patient_id = randint(1, 10000)

            u = User(first_name=first, last_name=last, patient_id=patient_id, group=randint(1,3))
            db.session.add(u)
            db.session.commit()
        print('{} of {}'.format(str(count), str(count)))

    def __repr__(self):
        return "User(patient_id={self.patient_id}, first_name={self.first_name_hash}, " \
               "last_name={self.last_name_hash})".format(self=self)

    def __str__(self):
        return self.__repr__()


class Protocol(db.Model):
    __tablename__ = 'protocol'
    id = db.Column(db.INTEGER, primary_key=True)
    form_id = db.Column(db.INTEGER, db.ForeignKey('form.id'))
    patient_id = db.Column(db.String, db.ForeignKey('user.patient_id'), index=True)
    row = db.Column(db.INTEGER)
    r_last_name = db.Column(db.String, db.ForeignKey('researcher.last_name'), index=True)
    protocol_type = db.Column(db.String)
    protocol_name_1 = db.Column(db.String)
    protocol_name_2 = db.Column(db.String)
    changes = db.Column(db.BOOLEAN, default=False)
    frequencies = db.Column(db.String)
    label = db.Column(db.String)
    duration = db.Column(db.String)
    game = db.Column(db.String)
    notes = db.Column(db.TEXT)

    form = db.relationship('Form', backref=backref('protocol', lazy='dynamic'))
    user = db.relationship('User', backref=backref('protocol', lazy='dynamic'))
    researcher = db.relationship('Researcher', backref=backref('protocol', lazy='dynamic'))

    def __repr__(self):
        return "Protocol(patient_id={self.patient_id}, row={self.row}, " \
               "researcher={self.r_last_name}, type={self.protocol_type}, " \
               "name={self.protocol_name_1}-{self.protocol_name_2}, frequencies={self.frequencies}, " \
               "label={self.label}, duration={self.duration}, notes={self.notes})".format(self=self)

    def __str__(self):
        return self.__repr__()


class Researcher(UserMixin, db.Model):
    __tablename__ = 'researcher'
    id = db.Column(db.INTEGER, primary_key=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    role = db.Column(db.String, default='admin')
    first_name = db.Column(db.String)
    last_name = db.Column(db.String, unique=True)
    token = db.Column(db.INTEGER, nullable=True)

    @property
    def password(self):
        raise AttributeError('password is hashed')

    @password.setter
    def password(self, p):
        self.password_hash = generate_password_hash(p)

    def verify_password(self, p):
        return check_password_hash(self.password_hash, p)

    def is_master(self):
        return self.role == 'master'

    def __repr__(self):
        return "Researcher(email={self.email}, first_name={self.first_name}, last_name={self.last_name})".format(self=self)

    @staticmethod
    def generate_token():
        from random import randint

        while True:
            to_ret = randint(10000, 99999)
            collision = Researcher.query \
                .filter(Researcher.token == to_ret) \
                .first()
            if collision is None:
                return to_ret

    @staticmethod
    def generate_researchers(count):
        import forgery_py
        from random import randint

        print('Generating researchers')
        for i in range(count):
            if i % 100 == 0:
                print('{} of {}'.format(str(i), str(count)))
            first = forgery_py.name.first_name().strip().lower()
            last = forgery_py.name.last_name().strip().lower()
            email = forgery_py.internet.email_address()
            password = forgery_py.address.city()
            role = 'admin' if randint(0,20) != 19 else 'master'
            r = Researcher(first_name=first, last_name=last, email=email, password=password,
                           role=role)
            db.session.add(r)
            db.session.commit()
        print('{} of {}'.format(str(count), str(count)))

@login_manager.user_loader
def load_user(user_id):
    return Researcher.query.get(int(user_id))