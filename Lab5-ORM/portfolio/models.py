from . import db
import enum
from datetime import datetime


class priorityEnum(enum.Enum):
    low, medium, high = 'low', 'medium', 'high'


class Task(db.Model):
    __tablename__ = "Tasks"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    created_at = db.Column(
        db.String, default=datetime.utcnow())
    deadline = db.Column(db.String)
    priority = db.Column(db.Enum(priorityEnum), default="high")
    is_done = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f"<Task-{self.id}\n \
        Title {self.title}\n \
        Description {self.description}\n \
        Created at {self.created_at}\n \
        Priority {self.priority}\n \
        Is done {self.is_done}>"
