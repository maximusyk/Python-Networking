from flask_wtf import FlaskForm, CSRFProtect
from flask_login import current_user
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
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


class UserUpdateForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])

    email = StringField('email', validators=[
        DataRequired(),
        Email()
    ])

    description = TextAreaField(
        "description",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
        render_kw={"rows": 3}
    )

    picture = FileField('Update Profile Photo', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'])
    ])

    def validate_username(self, field):
        if field.data != current_user.username:
            username = User.query.filter_by(username=field.data).first()
            if username:
                raise ValidationError(
                    "Username already taken. Please choose a different one.")

    def validate_email(self, field):
        if field.data != current_user.email:
            email = User.query.filter_by(email=field.data).first()
            if email:
                raise ValidationError(
                    "Email already taken. Please choose a different one.")


class ChangePasswordForm(FlaskForm):
    old_pwd = PasswordField('old_pwd', validators=[
        DataRequired(message="Password cannot be empty")])

    new_pwd = PasswordField('new_pwd', validators=[
        Length(min=6, message="The password cannot be less than 6 characters"),
        DataRequired(message="Password cannot be empty")])

    con_pwd = PasswordField('con_pwd', validators=[
        DataRequired(
            message="Passwords must match."),
        EqualTo('new_pwd', message="Passwords must match.")])
