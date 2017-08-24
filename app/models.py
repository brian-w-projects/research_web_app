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
import os
from config import config


class Form(db.Model):
    __tablename__ = 'form'
    id = db.Column(db.INTEGER, primary_key=True)
    session = db.Column(db.INTEGER, index=True)
    name = db.Column(db.String)
    date = db.Column(db.DateTime, index=True)
    patient_id = db.Column(db.String, db.ForeignKey('user.patient_id'))
    section = db.Column(db.INTEGER, default=0, nullable=True)

    user = db.relationship('User', backref=backref('form', lazy='dynamic'))

    def get_title(self):
        return ['Attention and Focus', 'Mood', 'Sleep', 'Communication and Connection', 'Energy',
                'Physical', 'Other'][self.section]

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
                       'Bed Wetting'],
                      ['Other (indicate in notes)',
                       'Other (indicate in notes)',
                       'Other (indicate in notes)']],
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
        form_date = datetime.utcnow().date() - timedelta(days=720)
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
            name = choice(['A'])
            f = Form(patient_id=u.patient_id,
                     date=form_date, name=name, session=s,
                     section=None)
            u.sessions += 1
            db.session.add(f)
            db.session.add(u)
            db.session.commit()
            f.section = None
            db.session.add(f)
            db.session.commit()
            for j in range(1,len([y for x in Form.get_questions(name) for y in x])+1):
                q = Question(form=f, question=j,
                             intensity=randint(0,4), frequency=randint(0,4),
                             change=randint(0,2),
                             notes=forgery_py.lorem_ipsum.sentences(randint(1,3)).replace(',','-').replace(';','-') if randint(1,5) == 2 else '')
                db.session.add(q)
            db.session.commit()
            form_date = form_date + timedelta(days=randint(1, 5))
            if form_date > datetime.utcnow().date():
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
    intake_page = db.Column(db.INTEGER, default=-1, nullable=True)
    initial_intake = db.Column(db.DateTime, default=datetime.utcnow())
    date_of_birth = db.Column(db.DateTime, nullable=True)
    eyes = db.Column(db.String, nullable=True)
    guardian_names = db.Column(db.String, nullable=True)
    custody = db.Column(db.String, nullable=True)
    gender = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    handed = db.Column(db.String, nullable=True)
    diagnosis = db.Column(db.String, nullable=True)
    reason_for_treatment = db.Column(db.String, nullable=True)
    current_medication = db.Column(db.String, nullable=True)
    previous_medication = db.Column(db.String, nullable=True)
    referral = db.Column(db.String, nullable=True)
    folder = db.Column(db.String, nullable=True, default=None)

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

    def create_folder(self):
        my_path = os.path.abspath(os.path.join(
            config[os.environ.get('CONFIG') or 'development'].UPLOADED_PATIENT_DEST, self.patient_id))
        if not os.path.exists(my_path):
            os.makedirs(my_path)
        self.folder=my_path

    @staticmethod
    def get_intake_questions():
        return ['Parents or Guardians Names', 'Custody', 'Gender', 'Address',
                 'Phone Number', 'Email Address', 'Handed (left, right or both)', 'Previous and current diagnosis',
                'Reason for Treatment', 'Current Medication (generic name, dosage, time of day)',
                'Previous Medication (generic name, dosage, time of day)', 'Source of Referral']

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
            u = User(first_name=first, last_name=last, patient_id=str(i), group=randint(1,3),
                     date_of_birth=datetime.strftime(forgery_py.date.date(past=True, min_delta=7000, max_delta=10000), '%m/%d/%Y'))
            db.session.add(u)
            db.session.commit()
            u.create_folder()
        print('{} of {}'.format(str(count), str(count)))

    def __repr__(self):
        return "User(patient_id={self.patient_id}, first_name={self.first_name_hash}, " \
               "last_name={self.last_name_hash}, phone={self.phone})".format(self=self)

    def __str__(self):
        return self.__repr__()


class Protocol(db.Model):
    __tablename__ = 'protocol'
    id = db.Column(db.INTEGER, primary_key=True)
    form_id = db.Column(db.INTEGER, db.ForeignKey('form.id'))
    patient_id = db.Column(db.String, db.ForeignKey('user.patient_id'), index=True)
    row = db.Column(db.INTEGER)
    r_last_name = db.Column(db.String, db.ForeignKey('researcher.last_name'), index=True)
    number = db.Column(db.String)
    protocol_type = db.Column(db.String)
    site_1 = db.Column(db.String)
    site_2 = db.Column(db.String)
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
               "name={self.site_1}-{self.site_2}, frequencies={self.frequencies}, " \
               "label={self.label}, duration={self.duration}, notes={self.notes})".format(self=self)

    def __str__(self):
        return self.__repr__()


class Intake(db.Model):
    __tablename__ = 'intake'
    id = db.Column(db.INTEGER, primary_key=True)
    patient_id = db.Column(db.String, db.ForeignKey('user.patient_id'), index=True)
    question = db.Column(db.INTEGER)
    answer = db.Column(db.String, nullable=True)
    details = db.Column(db.String)

    user = db.relationship('User', backref=backref('intake', lazy='dynamic'))

    @staticmethod
    def get_intake_questions():
        return [['Birth trauma and or hypoxia', 'Health problems during early childhood',
                 'Early development, such as started to talk, walk too late',
                 'Head trauma (with loss of consciousness)', 'Poor grades in school, poor performance at work'],
                ['Gastrointestinal disease (Gastirties, colities, etc.),'
                 'Cardiac and pulmonary disease (high blood pressure, arrtimias, etc.)',
                 'Neurological disease (tumors, isquemic events, etc)',
                 'Respiratory disease (asthma, bronquitis, etc)',
                 'Hospitalizations (dates and cause)',
                 'Surgeries (dates and cause)',
                 'Allergies (food, environment or medications)',
                 'Apetitie (low, uncontrollable, etc)'],
                ['Often having headaches and or migraines', 'Feels weak and passive during daytime',
                 'Sleep-related difficulties', 'Abuses alcohol or drugs', 'Has history of seizures'],
                ['Perceptual difficulties in vision, hearing, touch (dyslexia, paresis, etc.)',
                 'Difficulties in social interaction and communication, austistic spectrum',
                 'Motor-related difficulties, such as fine motor, tremor, rigidity, apraxia',
                 'Attention difficulties',
                 'Impulsiveness', 'Difficulties in correcting behavior', 'Psychosis (hallucinations, delusions, etc.)',
                 'Occupied by mostly positive thoughts, manic',
                 'Occupied by mostly negative thoughts, depressed',
                 'Anxious',
                 'Poor memory for recent events',
                 'Other forms of memory deficit'],
                ['Current therapies (type and dates)',
                 'Previous Therapies (types and dates)',
                 'Eats 3 or more meals a day',
                 'Types of food',
                 'Supplements']]

    def __repr__(self):
        return "Intake(patient_id={self.patient_id}, question={self.question}, answer={self.answer}," \
               "details={self.details}".format(self=self)

    def __str__(self):
        return self.__repr__()


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.INTEGER, primary_key=True)
    patient_id = db.Column(db.String, db.ForeignKey('user.patient_id'), index=True)
    filename = db.Column(db.String)
    researcher_last = db.Column(db.String, db.ForeignKey('researcher.last_name'), index=True)
    date = db.Column(db.Date, default=datetime.utcnow().date())

    user = db.relationship('User', backref=backref('file', lazy='dynamic'))
    researcher = db.relationship('Researcher', backref='file')

    def __repr__(self):
        return "File(patient_id={self.patient_id}, filename={self.filename}, " \
               "researcher_last={self.researcher_last})".format(self=self)

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
            try:
                r = Researcher(first_name=first, last_name=last, email=email, password=password,
                           role=role)
                db.session.add(r)
                db.session.commit()
            except:
                continue
        print('{} of {}'.format(str(count), str(count)))

@login_manager.user_loader
def load_user(user_id):
    return Researcher.query.get(int(user_id))