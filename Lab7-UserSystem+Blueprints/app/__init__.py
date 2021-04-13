from flask import Flask
from flask_wtf import CSRFProtect

# Blueprints
from .home import home
from .about import about
from .portfolio import portfolio
from .contact import contact
from .todo import todo
from .users import users

# Local Modules
from .database import db

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        db.create_all()

        app.register_blueprint(home.home_bp)
        app.register_blueprint(about.about_bp)
        app.register_blueprint(portfolio.portfolio_bp)
        app.register_blueprint(contact.contact_bp)
        app.register_blueprint(todo.todo_bp)
        app.register_blueprint(users.users_bp)

    # print("\n<<=== URL MAP ===>>")
    # print(app.url_map)
    # print()
    return app
