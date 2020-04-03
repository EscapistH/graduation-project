import os

from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app

conf = os.environ.get('FLASK_ENV', 'development')
app = create_app(conf)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
