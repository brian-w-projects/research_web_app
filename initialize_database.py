#!usr/bin/env python
import os
from app import create_app, db
from app.models import User, Form, Question, Researcher, Protocol
import shutil
from config import config

app = create_app(os.environ.get('CONFIG') or 'development')

if __name__ == '__main__':

    print("This script will initialize this app's databases")
    if input("Continue? (y/n) ") == 'y':
        print('WARNING: If you continue all databases will be wiped!')
        print('WARNING: You will NOT be able to retrieve database information')
        if input('Please confirm (CONFIRM) ') == 'CONFIRM':
            folder = config[os.environ.get('CONFIG') or 'development'].UPLOADED_PATIENT_DEST
            if not os.path.exists(folder):
                os.makedirs(folder)
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                if os.path.isfile(file_path):
                   os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            with app.app_context():
                db.drop_all()
                db.create_all()
                e = input('Master Account Email: ')
                p = input('Master Account Password: ')
                f = input('Master Account First Name: ')
                l = input('Master Account Last Name: ')
                r = Researcher(role='master', email=e, password=p, first_name=f,
                               last_name=l, token=None)
                db.session.add(r)
                db.session.commit()
                print('Databases Initialized')
        else:
            print('Initialization cancelled.')
    else:
        print('Initialization cancelled.')
        print('Initialization cancelled.')