from app import create_app, db
from app.models import User, Form, Question, Researcher, Protocol
import os
import csv


def create_users(folder):
    #create users
    file = os.path.abspath(os.path.join(folder, 'users.csv'))
    if not os.path.exists(file):
        print('users.csv file does not exist.')
        exit()
    with open(os.path.abspath(file), encoding='utf-8') as i:
        i_reader = csv.reader(i)
        id = -1

        for row in i_reader:
            if row[0] == id:
                continue
            else:
                try:
                    u = User(patient_id=row[0], first_name=row[1], last_name=row[2], group=row[3])
                    db.session.add(u)
                    db.session.commit()
                    id = row[0]
                except:
                    db.session.rollback()


app = create_app(os.environ.get('CONFIG') or 'development')
with app.app_context():
    folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'import'))
    if not os.path.exists(folder):
        os.makedirs(folder)
        print('import folder created. Place "users", "intensity", "frequency", "change" and "notes" csv files'
              'inside of this folder')
        exit()
    create_users(folder)

    i_file = os.path.abspath(os.path.join(folder, 'intensity.csv'))
    f_file = os.path.abspath(os.path.join(folder, 'frequency.csv'))
    c_file = os.path.abspath(os.path.join(folder, 'change.csv'))
    n_file = os.path.abspath(os.path.join(folder, 'notes.csv'))

    with open(i_file, encoding='utf-8') as i,\
            open(f_file, encoding='utf-8') as f, \
            open(c_file, encoding='utf-8') as c, \
            open(n_file, encoding='utf-8') as n:
        i_reader = csv.reader(i)
        f_reader = csv.reader(f)
        c_reader = csv.reader(c)
        n_reader = csv.reader(n)

        for row in zip(i_reader, f_reader, c_reader, n_reader):
            f = Form(patient_id=row[0][0], session=row[0][2], name='A', date=row[0][3], section=None)
            db.session.add(f)
            db.session.commit()
            for num in range(4, 46):
                notes_to_add = row[3][num] if len(row[3]) > num else ''
                q = Question(form_id=f.id, question=num-3, intensity=row[0][num], frequency=row[1][num],
                             change=row[2][num],
                             notes="{}".format(notes_to_add).replace(',','-').replace(';','-'))
                db.session.add(q)
                db.session.commit()
