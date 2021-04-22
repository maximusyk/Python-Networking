from app.extensions import db, login_manager
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256
from datetime import datetime


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = pbkdf2_sha256.hash(password)

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    description = db.Column(db.String())
    image_file = db.Column(db.String(), default="default.jpg", nullable=False)
    last_seen = db.Column(db.String(), default=datetime.now())

    admin = db.Column(db.Boolean())

    def verify_password(self, pwd):
        """
        Verify actual password with hashed
        """
        return pbkdf2_sha256.verify(pwd, self.password)

    def __repr__(self):
        return f"User('{self.username}','{self.email}'"
