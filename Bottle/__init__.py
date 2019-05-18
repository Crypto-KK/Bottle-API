
from flask import Flask
from Bottle.config.settings import config
from Bottle.models.base import db
from Bottle.api.v1 import create_blueprint_v1

from flask_mail import Mail
mail = Mail()

def register_blueprints(app):
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def register_extensions(app):
    db.init_app(app)
    mail.init_app(app)

def create_app(config_name='development'):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    return app