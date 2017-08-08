from app import create_app, db
from app.models import User, Form, Question, Researcher, Protocol
import os
import csv


def reset():
    db.drop_all()
    db.create_all()
    r = Researcher(role='master', email='p@p.com', password='asdfasdfasdf', first_name='master',
                   last_name='blaster', token=None)
    db.session.add(r)

def create_users():
    #create users
    with open('/home/brian/Desktop/intensity.csv', encoding='utf-8') as i:
        i_reader = csv.reader(i)
        id = -1

        for row in i_reader:
            if row[0] == id:
                continue
            else:
                u = User(patient_id=row[0], first_name='a', last_name='a', group=row[1])
                db.session.add(u)
                db.session.commit()
                id = row[0]


app = create_app(os.environ.get('CONFIG') or 'development')
with app.app_context():
    reset()
    create_users()

    with open('/home/brian/Desktop/intensity.csv', encoding='utf-8') as i,\
            open('/home/brian/Desktop/frequency.csv', encoding='utf-8') as f, \
            open('/home/brian/Desktop/change.csv', encoding='utf-8') as c, \
            open('/home/brian/Desktop/notes.csv', encoding='utf-8') as n:
        i_reader = csv.reader(i)
        f_reader = csv.reader(f)
        c_reader = csv.reader(c)
        n_reader = csv.reader(n)

        for row in zip(i_reader, f_reader, c_reader, n_reader):
            f = Form(patient_id=row[0][0], session=row[0][2], name='A', date=row[0][3], section=None)
            db.session.add(f)
            db.session.commit()
            for num in range(4, 46):
                q = Question(form_id=f.id, question=num-3, intensity=row[0][num], frequency=row[1][num],
                             change=row[2][num],
                             notes="{}".format(row[3][num]).replace(',','-').replace(';','-'))
                db.session.add(q)
                db.session.commit()
