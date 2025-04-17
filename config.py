import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ваш-очень-секретный-ключ'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False