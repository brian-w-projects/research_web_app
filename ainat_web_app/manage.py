#!usr/bin/env python
import os

from flask import request

from app import create_app, db
from app.models import User, Form, Question

app = create_app(os.environ.get('CONFIG') or 'development')

@app.url_defaults
def hashed_static_file(endpoint, values):
    if 'static' == endpoint or endpoint.endswith('.static'):
        filename = values.get('filename')
        if filename:
            blueprint = request.blueprint
            if '.' in endpoint:
                blueprint = endpoint.rsplit('.', 1)[0]
            static_folder = app.static_folder
            if blueprint and app.blueprints[blueprint].static_folder:
                static_folder = app.blueprints[blueprint].static_folder
            fp = os.path.join(static_folder, filename)
            if os.path.exists(fp):
                values['_'] = int(os.stat(fp).st_mtime)


if __name__ == '__main__':

    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
        # User.generate_users(100)
        # u = User(first_name='bob', last_name='bob')
        # db.session.add(u)
        # db.session.commit()

        # Form.generate_forms(300)


    app.run(port=5000)
