from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from portfolio import app, db
from portfolio import models

migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
