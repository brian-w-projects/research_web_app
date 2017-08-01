import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    pass

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'asdlfasdflkjsdf'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/data.sqlite')
    SQLALCHEMY_DATABASE_URI = 'postgresql://brian:secret@localhost/brian'
    ENCRYPT_KEY = b'gv37r0qv6EGKcRJz64QOzct578GDISQlEgTmZrhOB7E='


class DeploymentConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    ENCRYPT_KEY = os.environ.get('ENCRYPT_KEY').encode('utf-8')


config = {
    'development': DevelopmentConfig,
    'deployment': DeploymentConfig
}
