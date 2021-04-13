from app.database import db
from passlib.hash import pbkdf2_sha256


class User(db.Model):
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = pbkdf2_sha256.hash(password)

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def verify_password(self, pwd):
        """
        Verify actual password with hashed
        """
        return pbkdf2_sha256.verify(pwd, self.password)

    def __repr__(self):
        return f"User('{self.username}','{self.email}'"
