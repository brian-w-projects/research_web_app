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
        return {'A': ['Attention and Focus', 'Mood', 'Sleep', 'Communication and Connection', 'Energy',
                'Physical', 'Other'],
                'B': ['Basal Ganglia', 'Cingulate Cortex', 'Temporal Lobes', 'Prefrontal Cortex', 'Deep Limbic System'],
                'C': ['Underarousal', 'Overarousal', 'Unstable Arousal'],
                'D': ['Page 1', 'Page 2', 'Page 3', 'Page 4', 'Page 5', 'Page 6', 'Page 7',
                      'Page 8', 'Page 9', 'Page 10', 'Page 11', 'Page 12',
                      'Page 13', 'Page 14']}.get(self.name)[self.section]

    def get_questions(self):
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
                'B': [['Frequent feelings of nervousness or anxiety',
                       'Panic Attacks',
                       'Symptoms of heightened muscle tension',
                       'Period of heart pounding, rapid heart rate or chest pain',
                       'Periods of trouble breathing or feeling smothered',
                       'Periods of feeling dizzy, faint or unsteady on your feet',
                       'Periods of nausea or abdominal upset',
                       'Periods of sweating, hot or cold flashes',
                       'Tendency to predict the worst',
                       'Fear of dying or doing something crazy',
                       'Avoid places for fear of having an anxiety attack',
                       'Conflict avoidance',
                       'Excessive fear of being judged or scrutinized by others',
                       'Persistent phobias',
                       'Low motivation',
                       'Excessive motivation',
                       'Tics',
                       'Poor handwriting',
                       'Quick startle',
                       'Tendency to freeze',
                       'Lacks confidence in their abilities',
                       'Seems shy or timid',
                       'Easily embarrassed'],
                      ['Excessive or senseless worrying',
                       'Upset when things do not go your way',
                       'Upset when things are out of place',
                       'Tendency to be oppositional or argumentative',
                       'Tendency to have repetitive, negative thoughts',
                       'Tendency toward compulsive behaviors',
                       'Intense dislike for change',
                       'Tendency to hold grudges',
                       'Trouble shfiting attention from subject to subject',
                       'Trouble shifting behaviour from task to task',
                       'Difficulties seeing options in situations',
                       'Tendency to hold on to own opinion and not listen to others',
                       'Tendency to get locked into a course of action whether or not it is good',
                       'Needing to have things done a certain way or you become upset',
                       'Others complain that you worry too much',
                       'Tend to say not without first thinking about questions',
                       'Tendency to predict fear'],
                      ['Short fuse or periods of extreme irritability',
                       'Periods of rage with little provocation',
                       'Often misinterprets comments as negative when they are not',
                       'Irritability tends ot build, then explodes, then redcedes, often tired after a rage',
                       'Periods of panic and or fear for not specific reasons',
                       'Visual or auditory changes',
                       'Frequent periods of deja vu',
                       'Sensitivity or mild paranoia',
                       'Headaches or abdominal pain of uncertain origin',
                       'History of a head injury or family history of violence or explosiveness',
                       'Dark thoughts, may involve suicidal or homicidal thoughts',
                       'Periods of forgetfulness or memory problems',
                       'Difficulties with memory',
                       'Difficulties to understand a reading text',
                       'Mainly occupied with ethical or religious ideas'],
                      ['Fails to give attention to details or makes careless mistakes',
                       'Trouble sustaining attention in routine situations',
                       'Trouble listening',
                       'Fails to finish things',
                       'Poor organization for time or space',
                       'Forgetful',
                       'Poor planning skills',
                       'Lack clear goals or forward thinking',
                       'Difficulty expressing feelings',
                       'Difficulty expressing empathy for others',
                       'Excessive daydreaming',
                       'Feeling bored',
                       'Feeling apathetic or unmotivated',
                       'Feeling tired, sluggish or slow moving',
                       'Feeling spacey or "in a fog"',
                       'Difficulty playing quietly',
                       'Loses things',
                       'On the go or acts as if "driven by a motor"',
                       'Talks excessively',
                       'Blurts out answers before questions have been completed',
                       'Difficulty waiting your turn',
                       'Interrupts or intrudes on others',
                       'Impulsive',
                       'Difficulty to learn from mistakes. Tends to make same mistakes over and over'],
                      ['Frequent feelings of sadness',
                       'Moodiness',
                       'Negativity',
                       'Low energy',
                       'Irritability',
                       'Decreased interest in others',
                       'Feelings of hopelessness about the future',
                       'Feelings of helplessness or powerlessness',
                       'Feeling of dissatisfied or bored',
                       'Excessive guilt',
                       'Suicidal feelings',
                       'Crying spells',
                       'Decreased interest in things that are usually fun or pleasurable',
                       'Sleep changes',
                       'Appetite changes',
                       'Chronic low self-esteem',
                       'Low interest in sexuality',
                       'Negative sensitivity to smells or odors',
                       'Forgetful',
                       'Difficulties with concentration']],
                'C': [['ADD Diagnosis',
                       'Poor concentration',
                       'Inattentive',
                       'Distractibility',
                       'Frequent daydreaming',
                       'Spaciness or fogginess',
                       'Forgetful',
                       'Confused thinking',
                       'Lack of motivation',
                       'Depression or low mood',
                       'Lethargy',
                       'Sensitive, feelings eaisly hurt',
                       'Tears easily',
                       'Low self-esteem',
                       'Tends ot introversion',
                       'Excessive shy',
                       'Frequent waking at night',
                       'Not feeling rested after sleep',
                       'Sleep more than 9 hours a night',
                       'Falls asleep in low stimulation situations',
                       'Snores without apnea',
                       'Likes caffeine',
                       'Dislikes alcohol effects'],
                      ['Busy mind or many competing thoughts',
                       'Impulsive',
                       'Fidgety',
                       'Hyperactive',
                       'Easily bored',
                       'Risk seeker',
                       'Impatient',
                       'Agitated',
                       'Aggressive',
                       'Angry depression',
                       'Anxious/fearful',
                       'Tense',
                       'Feel overwhelmed',
                       'Frequent tension headaches',
                       'Teeth grinding or clinching',
                       'Holds resentments',
                       'Many social conflicts',
                       'Difficulty falling asleep',
                       'Sensory overload',
                       'Low emotional awareness',
                       'Heart palpitations',
                       'Dislikes caffeine',
                       'Likes alcohol effects',
                       'Menopausal hot flashes'],
                      ['History of seizures',
                       'History of head injury',
                       'Migraine headaches',
                       'Bipolar symptoms',
                       'Chronic fatigue symptoms',
                       'Wakes during night or light sleeps',
                       'Sleep Apnea',
                       'Sleepwalking now or as a child',
                       'Frequent nightmares',
                       'Bedwetting after conventional age',
                       'Night sweats',
                       'Hot flashes nor related to menopause',
                       'Psychiatric illness in family',
                       'PMS symptoms',
                       'Relationship issues or diagnosed with personality disorder',
                       'Poor eye contact'],],
                'D': [['(1) Thinks clearly -- (7) Difficulty Thinking',
                       '(1) Creative Problem Solver -- (7) Gets stuck with Problems',
                       '(1) Plans Effectively -- (7) Does not plan',
                       '(1) Good decision-maker -- (7) Cant make up mind',
                       '(1) Organizes tasks effectively -- (7) Does not organize tasks well',
                       '(1) Detail oriented -- (7) Struggles with details',
                       '(1) Careful and accurate -- (7) Makes careless mistakes',
                       '(1) Maintains attention on task -- (7) Easily distracted from task',
                       '(1) Good listener -- (7) Poor listener',
                       '(1) Follows Instructions -- (7) Does not follow instructions'],
                      ['(1) Remembers tasks and appointments -- (7) Forgets tasks and appointments',
                       '(1) Alert to surroundings -- (7) Daydreamy',
                       '(1) Completes tasks -- (7) Starts but does not finish',
                       '(1) Keeps track of items -- (7) Loses or misplaces things',
                       '(1) Positive and happy -- (7) Negative and unhappy',
                       '(1) Comfortable in social situations -- (7) Uncomfortable socially',
                       '(1) Feels good about self -- (7) Poor self image',
                       '(1) Handles new situations confidently -- (7) Dislikes new situations',
                       '(1) Energetic and enthusiastic -- (7) Low energy',
                       '(1) Eats appropriately -- (7) Eats little or overeats'],
                      ['(1) Sleeps easily and gets up easily -- (7) Sleeps little or too much',
                       '(1) Generally calm and stable -- (7) Agitated or irritable',
                       '(1) Positive about the future -- (7) Hopeless about future',
                       '(1) Finds enjoyment and pleasure in life -- (7) Cannot see positives in life',
                       '(1) Sees positive traits in others -- (7) Negative view of others',
                       '(1) Happy and joyful -- (7) Flat or unhappy',
                       '(1) Laughs easily and appropriately -- (7) Rarely laughs',
                       '(1) Experiences excitement in life -- (7) Finds life boring',
                       '(1) Has good vocabulary and uses it well -- (7) Limited Vocabulary',
                       '(1) Speaks in complete and orderly way -- (7) Disorganized verbal expression'],
                      ['(1) Clear, expressive writer -- (7) Writes poorly',
                       '(1) Accurate grammar and punctuation -- (7) Makes grammar or punctuation errors',
                       '(1) Recalls desired words when writing -- (7) Cannot find the right word',
                       '(1) Self-starter who gets things done -- (7) Unmotivated',
                       '(1) Participates in recreational activities -- (7) Does not participate',
                       '(1) Interested in other people -- (7) Finds others boring',
                       '(1) Interested in word or school -- (7) Finds school or work boring',
                       '(1) Has goals and plans in life -- (7) Just goes through life',
                       '(1) Able to deviate from routine -- (7) Stuck in routine ways of doing things',
                       '(1) Tolerates disorder -- (7) Greatly disturbed by disorder'],
                      ['(1) Allows others control -- (7) Needs to control people and situations',
                       '(1) Not perfectionistic -- (7) Demands Perfection',
                       '(1) Balances work with social life -- (7) Obsession with work crowds out social life',
                       '(1) Adjusts to new experiences -- (7) Cannot shift patterns for doing things',
                       '(1) Flexible behavior and speech patterns -- (7) Compulsive repetition of speech',
                       '(1) Able to do things quickly and accurately -- (7) Works very slowly to be sure things are right',
                       '(1) Does not have obsessive thoughts -- (7) Cannot stop unpleasant repetitive thoughts',
                       '(1) Flexible -- (7) Stubborn',
                       '(1) Follows the rules -- (7) Disobedient',
                       '(1) Accepts authority -- (7) Rebels against authority'],
                      ['(1) Not argumentative -- (7) Argues for the sake of arguing',
                       '(1) Does not do things to annoy others -- (7) Does things just to bother others',
                       '(1) Able to control temper -- (7) Poor temper control',
                       '(1) Accepts responsibility for own actions -- (7) Blames others',
                       '(1) Not easily annoyed -- (7) Annoyed by small things',
                       '(1) Calm and positive -- (7) Angry or resentful',
                       '(1) Treats others compassionately -- (7) Does things to hurt others',
                       '(1) Controls use of substances -- (7) Addictive with certain substances',
                       '(1) Controls behaviors -- (7) Cannot control certain behaviors',
                       '(1) Able to stop use of substances -- (7) Feels discomfort when attempting to stop using'],
                      ['(1) Thinks before acting -- (7) Impulsive actions',
                       '(1) Controls temper in public -- (7) Loses temper in public',
                       '(1) Appropriate expressions of sexuality -- (7) Inappropriate sexual activity',
                       '(1) Does not argue or fight -- (7) Argumentative or gets into fights',
                       '(1) Controls physical behavior when angry -- (7) Physically out of control when angry',
                       '(1) Does not interrupt in conversations -- (7) Interrupts often',
                       '(1) Can wait in line or do things in turn -- (7) Impatient when required to wait',
                       '(1) Need not be center of attention -- (7) Seeks attention in groups',
                       '(1) Respects feelings of others -- (7) Speaks without thinking of others feelings',
                       '(1) Finishes tasks without jumping around -- (7) Cannot stay on task to completion'],
                      ['(1) Feels fear when appropriate -- (7) Not afraid when others would be ',
                       '(1) Feels anger when appropriate -- (7) Does not get angry when others would',
                       '(1) Feels anxious when appropriate -- (7) Does not get nervous when others would',
                       '(1) Not needlessly frightened -- (7) Afraid in situations when others are not',
                       '(1) Anger level is appropriate to the cause -- (7) Overreacts to anger-proviking situations',
                       '(1) Recalls childhood clearly -- (7) Has lost periods of time from childhood',
                       '(1) Feels pain appropriately -- (7) Does not feel pain when others would',
                       '(1) Does not hear voices in head -- (7) Hears voices in head',
                       '(1) Able to sit still -- (7) Fidgety and restless'],
                      ['(1) Appropriate level of energy -- (7) Sluggish or low energy',
                       '(1) Talks appropriately -- (7) Talks excessively or very little',
                       '(1) Talks at reasonable pace -- (7) Talks very fast or very slowly',
                       '(1) Can entertain self quietly -- (7) Cannot relax or work or play quietly',
                       '(1) Able to start new tasks -- (7) Cannot find the energy to get things started',
                       '(1) Clear handwriting -- (7) Messy Handwriting',
                       '(1) Able to do fine-motor tasks -- (7) Difficulty with fine-motor tasks',
                       '(1) Graceful and coordinated -- (7) Clumsy, breaks or bumps into things',
                       '(1) Balanced and Rhythmic -- (7) Poor balance or rhythm',
                       '(1) Feels ashamed when appropriate -- (7) Feels shame inappropriately'],
                      ['(1) Feels guilty when appropriate -- (7) Feels guilt without reason',
                       '(1) Does not blame self -- (7) Blames self for things that go wrong',
                       '(1) Satisfied with good performance -- (7) Never satisfied with performance',
                       '(1) Hears words clearly -- (7) Hears words as jumbled',
                       '(1) Listens effectively -- (7) Misses words when listening',
                       '(1) Repeats accurately what is heard -- (7) Difficulty repeating what has been said',
                       '(1) Follows spoken instructions -- (7) Difficulty repeating what has been said',
                       '(1) Follows conversations -- (7) Hard time following discussions',
                       '(1) Understands what people say -- (7) Misunderstand what people say',
                       '(1) Recalls heard information -- (7) Quickly forgets heard information'],
                      ['(1) Remembers names of acquaintances -- (7) Forgets names of people known for a long time',
                       '(1) Reads aloud accurately -- (7) Skips or substitutes words when reading aloud',
                       '(1) Reads at appropriate speed -- (7) Reads slowly for age',
                       '(1) Reads at appropriate level -- (7) Difficulty reading at appropriate level',
                       '(1) Sees words clearly -- (7) Cannot easily distinguish between words visually',
                       '(1) Recognizes letters clearly -- (7) Confuses letters that look somewhat alike',
                       '(1) No letter, number or word reversal -- (7) Reverse letters, numbers or words',
                       '(1) Spelling appropriate to age level -- (7) Poor speller for age level',
                       '(1) Understand what is read -- (7) Reads words but does not understand them',
                       '(1) Can repeat read material -- (7) Cannot repeat or explain what was just read'],
                      ['(1) Comprehends read material -- (7) Difficulty with comprehension of read material',
                       '(1) Well coordinated in movements -- (7) Movements uncoordinated',
                       '(1) Move smoothly and decisively -- (7) Movement hesitant or jerky',
                       '(1) Aware of body position and location -- (7) Unaware of own body position',
                       '(1) Appropriately sensitive to touch -- (7) Extreme or very little sensitivity to touch',
                       '(1) Copies numbers accurately -- (7) Makes errors copying numbers',
                       '(1) Rarely makes ismple calculation errors -- (7) Makes careless calculation errors',
                       '(1) Completes multi-step math problems -- (7) Cannot perform multi-step calculations',
                       '(1) Counts easily and without errors -- (7) Difficulty counting',
                       '(1) Does not reverse numbers -- (7) Reverses numbers'],
                      ['(1) Understands math concepts easily -- (7) Does not understand math concepts',
                       '(1) Works well with building projects -- (7) Not able to build accurately',
                       '(1) Puts together puzzle pieces easily -- (7) Difficulty with puzzles',
                       '(1) Catches balls without difficulty -- (7) Difficulty catching balls',
                       '(1) Can hit or kick a moving ball -- (7) Difficulty with moving balls',
                       '(1) Accurately copies form written material -- (7) Makes errors copying spoken material',
                       '(1) Does not over-respond to minor scares -- (7) Easily frightened',
                       '(1) Responds without excessive anger -- (7) Overreacts to anger-proviking situations',
                       '(1) Not generally fearful -- (7) Fearful much of the time'],
                      ['(1) Not generally angry -- (7) Angry much of the time',
                       '(1) Rarely becomes enraged -- (7) Easily enraged',
                       '(1) Gets non-verbal meaning of speech -- (7) Misses the sense of what is said',
                       '(1) Recognizes differences between voices -- (7) Confuses voices',
                       '(1) Recognizes mood from tone of voice -- (7) Not tuned in to others moods',
                       '(1) Knows when others are kidding -- (7) Misses jokes and kidding',
                       '(1) Good memory for faces -- (7) Easily forgets faces',
                       '(1) Gives directions clearly and accurately -- (7) Cannot give directions clearly',
                       '(1) Rarely loses keys or glasses -- (7) Loses routine items often',
                       '(1) Awakens to go to bathroom -- (7) Wets bed at night',
                       '(1) Does not grind teeth in sleep -- (7) Grinds teeth at night',
                       '(1) Sleeps quietly -- (7) Restless sleeper',
                       '(1) Awakes feeling rested -- (7) Tired even after sleeping']
                      ]}.get(self.name)

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


class Cortical(db.Model):
    __tablename__ = 'cortical'
    id = db.Column(db.INTEGER, primary_key=True)
    form_id = db.Column(db.INTEGER, db.ForeignKey('form.id'))
    question = db.Column(db.INTEGER)
    response = db.Column(db.String, default='')

    form = db.relationship('Form', backref=backref('cortical', lazy='dynamic'))

    def __repr__(self):
        return "Cortical(form_id={self.form_id}, question={self.question}, response={self.response})" \
            .format(self=self)

    def __str__(self):
        return self.__repr__()


class Arousal(db.Model):
    __tablename__ = 'arousal'
    id = db.Column(db.INTEGER, primary_key=True)
    form_id = db.Column(db.INTEGER, db.ForeignKey('form.id'))
    question = db.Column(db.INTEGER)
    response = db.Column(db.String, default='')

    form = db.relationship('Form', backref=backref('arousal', lazy='dynamic'))

    def __repr__(self):
        return "Arousal(form_id={self.form_id}, question={self.question}, response={self.response})"\
            .format(self=self)

    def __str__(self):
        return self.__repr__()


class Major(db.Model):
    __tablename__ = 'major'
    id = db.Column(db.INTEGER, primary_key=True)
    form_id = db.Column(db.INTEGER, db.ForeignKey('form.id'))
    question = db.Column(db.INTEGER)
    response = db.Column(db.String, default='')

    form = db.relationship('Form', backref=backref('major', lazy='dynamic'))

    def __repr__(self):
        return "Major(form_id={self.form_id}, question={self.question}, response={self.response})" \
            .format(self=self)

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
                r = Researcher(first_name=first, last_name=last, email=email, password=password, role=role)
                db.session.add(r)
                db.session.commit()
            except:
                continue
        print('{} of {}'.format(str(count), str(count)))

@login_manager.user_loader
def load_user(user_id):
    return Researcher.query.get(int(user_id))