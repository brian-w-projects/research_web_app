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
    SQLALCHEMY_DATABASE_URI = 'postgresql://brian:secret@localhost/brian'
    UPLOADED_PATIENT_DEST = os.path.abspath(os.path.join(os.path.dirname(__file__),'patient_files'))
    # ENCRYPT_KEY = b'gv37r0qv6EGKcRJz64QOzct578GDISQlEgTmZrhOB7E='



class DeploymentConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') if 'SECRET_KEY' in os.environ else None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') if 'DATABASE_URL' in os.environ else None
    UPLOADED_PATIENT_DEST = os.path.abspath(os.path.join(os.path.dirname(__file__), 'patient_files'))
    # ENCRYPT_KEY = os.environ.get('ENCRYPT_KEY').encode('utf-8') if 'ENCRYPT_KEY' in os.environ else None


config = {
    'development': DevelopmentConfig,
    'deployment': DeploymentConfig
}
