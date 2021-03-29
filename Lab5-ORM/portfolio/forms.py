from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, SelectField, BooleanField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length

csrf = CSRFProtect()

PRIORITY_CHOICES = [("high", "high"), ("medium", "medium"), ("low", "low")]


class ContactForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired(message="Name cannot be empty")]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="E-mail cannot be empty"),
            Email("Enter a valid email(abc@example.xyz)"),
        ],
    )
    subject = StringField(
        "Subject", validators=[DataRequired(message="Subject cannot be empty")]
    )
    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Message cannot be empty"),
            Length(min=2, max=100),
        ],
    )


class TaskForm(FlaskForm):
    title = StringField(
        "title",
        validators=[DataRequired(message="Title cannot be empty")]
    )
    description = TextAreaField(
        "description",
        validators=[
            DataRequired(message="Description cannot be empty"),
            Length(min=2, max=100),
        ],
        render_kw={"rows": 3}
    )
    priority = SelectField("priority", choices=PRIORITY_CHOICES)
    timeline = StringField("timeline")
    is_done = BooleanField('is_done')


# class UpdateTaskForm(FlaskForm):
#     title = StringField(
#         "Title", validators=[DataRequired(message="Title cannot be empty")]
#     )
#     description = TextAreaField(
#         "Description",
#         validators=[
#             DataRequired(message="Description cannot be empty"),
#             Length(min=2, max=100),
#         ],
#     )
#     priority = SelectField("Priority", choices=PRIORITY_CHOICES)
