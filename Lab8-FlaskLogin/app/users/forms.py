from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
from .models import User

csrf = CSRFProtect()


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[
        Length(min=4, max=25, message="Username must contain 4-25 characters"),
        DataRequired(message="This field cannot be empty")])
    email_up = StringField('email_up', validators=[
        DataRequired(message="Email cannot be empty"),
        Email()])
    password_up = PasswordField('password_up', validators=[
        Length(min=6, message="The password cannot be less than 6 characters"),
        DataRequired(message="Password cannot be empty")])
    confirm_password = PasswordField('conf_password', validators=[
                                     DataRequired(
                                         message="Passwords must match."),
                                     EqualTo('password_up', message="Passwords must match.")])

    def validate_email_up(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already taken")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already taken")


class LoginForm(FlaskForm):
    email_in = StringField('email_in', validators=[
        DataRequired(message="Username cannot be empty")
    ])
    password_in = PasswordField('password_in', validators=[
        DataRequired(message="Password cannot be empty")])
    remember_me = BooleanField('remember_me')
