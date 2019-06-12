from datetime import datetime, date
from decimal import Decimal

from flask import Flask, g

from flask.json import JSONEncoder as _JSONEncoder
from Bottle.errors.error_code import ServerError
from Bottle.config.settings import config
from Bottle.models.base import db
from Bottle.api.v1 import create_blueprint_v1
from extensions import mail, limiter


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, Decimal):
            return str(o)
        raise ServerError()


def register_blueprints(app):
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def register_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)


def monkey_patch(app):
    app.json_encoder = JSONEncoder


def create_app(config_name='development'):
    app = Flask(__name__)
    monkey_patch(app)
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    return app
