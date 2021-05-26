from app.extensions import csrf
from app.task_api import api_bp
from app.todo.models import *
from flask import jsonify, request

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@api_bp.route("/tasks", methods=["POST"])
@csrf.exempt
def create_task():
    title = request.json["title"]
    description = request.json["description"]
    priority = request.json["priority"]
    category_id = request.json["category_id"]

    new_task = Task(title=title, description=description, priority=priority, category_id=category_id)

    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)


@api_bp.route("/tasks", methods=["GET"])
@csrf.exempt
def get_tasks():
    all_tasks = Task.query.all()

    return tasks_schema.jsonify(all_tasks)


@api_bp.route("/tasks/<id>", methods=["GET"])
@csrf.exempt
def get_task(id):
    task = Task.query.get(id)

    return task_schema.jsonify(task)


@api_bp.route("/tasks/<id>", methods=["PUT"])
@csrf.exempt
def update_task(id):
    task = Task.query.get(id)

    title = request.json["title"]
    description = request.json["description"]
    priority = request.json["priority"]
    category_id = request.json["category_id"]

    task.title = title
    task.description = description
    task.priority = priority
    task.category_id = category_id

    db.session.commit()

    return task_schema.jsonify(task)


@api_bp.route("/tasks/<id>", methods=["DELETE"])
@csrf.exempt
def delete_product(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)
