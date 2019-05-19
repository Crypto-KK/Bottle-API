from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from Bottle import db
from server import app
from Bottle.models.user import User
from Bottle.models.movie import NewMovie, HotMovie, ClassicMovie
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
