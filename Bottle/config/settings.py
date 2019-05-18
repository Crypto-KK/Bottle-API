import os
import sys

from dotenv import find_dotenv, load_dotenv


base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(base_dir, 'Bottle'))
load_dotenv(find_dotenv())


class BaseConfig:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
    MAIL_USE_TSL = os.getenv('MAIL_USE_TSL')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_SENDER = os.getenv('MAIL_SENDER')


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(BaseConfig):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}