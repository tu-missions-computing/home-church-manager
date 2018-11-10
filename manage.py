import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from application import app, adb


#app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, adb)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
