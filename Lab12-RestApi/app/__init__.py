from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager

from .about import about
from .admin import create_admin
from .contact import contact

# Local Modules
from .extensions import csrf, db, login_manager, ma

# Blueprints
from .home import home
from .portfolio import portfolio
from .task_api import api
from .todo import todo
from .users import users


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevelopmentConfig")

    db.init_app(app)
    ma.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    create_admin(app)

    with app.app_context():
        db.create_all()

        app.register_blueprint(home.home_bp)
        app.register_blueprint(about.about_bp)
        app.register_blueprint(portfolio.portfolio_bp)
        app.register_blueprint(contact.contact_bp)
        app.register_blueprint(todo.todo_bp)
        app.register_blueprint(users.users_bp)
        app.register_blueprint(api.api_bp, url_prefix="/api")

    # print("\n<<=== URL MAP ===>>")
    # print(app.url_map)
    # print()
    return app
