import json
import os
import sys
from datetime import date, datetime

from flask import flash, redirect, render_template, request, session, url_for, jsonify
from flask_mail import Mail, Message

from . import app, db
from .forms import *
from .models import Task, priorityEnum

mail = Mail()
csrf.init_app(app)
mail.init_app(app)

menu = [
    ("Home", "/", "home"),
    ("About", "/about", "user"),
    ("Portfolio", "/portfolio", "book-content"),
    ("Contact", "/contact", "envelope"),
    ("ToDo List", "/todo", "list-check"),
]

currDate = date.today()


def writeJSON(data, filename="dump.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


@app.route("/")
@app.route("/hero")
def index():
    return render_template(
        "index.html",
        menu=menu,
        my_os=os.uname(),
        user_agent=request.headers.get("User-Agent"),
        version=sys.version,
        time_now=datetime.now().strftime("%H:%M"),
    )


@app.route("/about")
def about():
    return render_template(
        "about.html",
        menu=menu,
        my_os=os.uname(),
        user_agent=request.headers.get("User-Agent"),
        version=sys.version,
        time_now=datetime.now().strftime("%H:%M"),
    )


@app.route("/portfolio")
def portfolio():
    session.clear()
    return render_template(
        "portfolio.html",
        menu=menu,
        my_os=os.uname(),
        user_agent=request.headers.get("User-Agent"),
        version=sys.version,
        time_now=datetime.now().strftime("%H:%M"),
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "POST":
        if "name" in session and "email" in session:
            print(
                f"Name -> {session.get('name')}\nEmail -> {session.get('email')}")
            form.name.data = session.get("name")
            form.email.data = session.get("email")
            if form.validate_on_submit():
                sbj = request.form["subject"]
                msg = request.form["message"]
                with open("dump.json") as jsonFile:
                    data = json.load(jsonFile)
                    temp = data["usrMessages"]
                    temp.append(
                        {
                            "Name": form.name.data,
                            "Email": form.email.data,
                            "Subject": form.subject.data,
                            "Message": form.message.data,
                        }
                    )
                writeJSON(data)
                flash("Your message has been sent. Thank you!", "message")
                return redirect(url_for("contact"))
            else:
                flash("There were some issues sending the message!", "error")
        else:
            if form.validate_on_submit():
                usrName = form.name.data
                usrEmail = form.email.data
                sbj = form.subject.data
                msg = form.message.data
                session["name"] = usrName
                session["email"] = usrEmail
                with open("dump.json") as jsonFile:
                    data = json.load(jsonFile)
                    temp = data["usrMessages"]
                    temp.append(
                        {
                            "Name": form.name.data,
                            "Email": form.email.data,
                            "Subject": form.subject.data,
                            "Message": form.message.data,
                        }
                    )
                writeJSON(data)
                flash("Your message has been sent. Thank you!", "message")
                return redirect(url_for("contact"))
            else:
                flash("There were some issues sending the message!", "error")
    return render_template(
        "contact.html",
        menu=menu,
        form=form,
        reqMethod=request.method,
        my_os=os.uname(),
        user_agent=request.headers.get("User-Agent"),
        version=sys.version,
        time_now=datetime.now().strftime("%H:%M"),
    )


def getTaskList():
    lowList, mediumList, highList, doneList = [], [], [], []
    if len(Task.query.all()) != 0:
        todos = Task.query.all()
        for item in todos:
            if item.is_done == 1:
                doneList.append(item)
            elif item.priority.value == 'low':
                lowList.append(item)
            elif item.priority.value == 'medium':
                mediumList.append(item)
            else:
                highList.append(item)
        return [highList, mediumList, lowList, doneList]
    else:
        return ''


@app.route("/todo/create", methods=["GET", "POST"], endpoint='create')
@app.route("/todo", methods=["GET", "POST"])
@app.route("/todo/<int:todo_id>", methods=["GET", "POST"], endpoint='view')
@app.route("/todo/<int:todo_id>/update", methods=["GET", "POST"], endpoint='update')
@app.route("/todo/<int:todo_id>/delete", methods=["GET", "POST"], endpoint='delete')
@app.route("/todo/<int:todo_id>/getById", methods=["GET", "POST"], endpoint='getById')
@app.route("/todo/<int:todo_id>/markTodo", methods=["GET", "POST"], endpoint='markTodo')
def todo(todo_id=None):
    # Index page allows to add new tasks, see these tasks, edit and deleted them.
    form = TaskForm()
    todos = getTaskList()
    # Get data from db by Id
    if request.endpoint == 'getById':
        task = Task.query.get_or_404(todo_id)
        print("<<<==== GET BY ID ====>>>")
        return json.dumps({
            'title': task.title,
            'description': task.description,
            'priority': task.priority.value,
            'timeline': task.created_at+" - "+task.deadline,
            'is_done': task.is_done
        })
    if request.endpoint == 'view':
        task = Task.query.get_or_404(todo_id)
        print("<<<==== VIEW BY ID ====>>>")
        return json.dumps({
            'Id': task.id,
            'Title': task.title,
            'Description': task.description,
            'Priority': task.priority.value,
            'Created': task.created_at,
            'Deadline': task.deadline,
            'Status': task.is_done
        })

    # Add new task
    if request.endpoint == 'create':
        print(f"\n====Adding new task was started....")
        if request.method == "POST":
            print("\n====METHOD POST.")
            if form.validate_on_submit():
                print("\n====VALIDATION COMPLETE.")
                task = Task(title=request.form['title'], description=request.form['description'],
                            priority=request.form['priority'], created_at=request.form['timeline'].split(" - ")[0], deadline=request.form['timeline'].split(" - ")[1])
                try:
                    db.session.add(task)
                    db.session.commit()
                    print("\n====TASK ADDED.")
                    return json.dumps(
                        {'success': 'true', 'msg': 'Task has been added successfully.', 'data': render_template('tasklist.html', todos=getTaskList())})
                except Exception as err:
                    db.session.rollback()
                    # flash("There are some issues adding the task!!", "error")
                    print("\n====ERROR ADDED TASK.")
                    print(err)
                    return json.dumps(
                        {'success': 'false', 'msg': 'There are some issues adding the task!!', 'data': form.data, 'errors': form.errors})
            else:
                print("\n====VALIDATION FAILED.")
                return json.dumps(
                    {'success': 'false', 'msg': 'Validation failed.', 'data': form.data, 'errors': form.errors})
    # Edit task by ID
    if request.endpoint == 'update':
        print(f"Update task-{todo_id} was started....")
        task = Task.query.get_or_404(todo_id)
        if form.validate_on_submit():
            task.title = request.form['title']
            task.description = request.form['description']
            task.priority = request.form['priority']
            task.created_at = request.form['timeline'].split(" - ")[0]
            task.deadline = request.form['timeline'].split(" - ")[1]
            task.is_done = 1 if 'is_done' in request.form else 0
            try:
                db.session.commit()
                print(f"Task-{todo_id} was updated successfully.")
                print(getTaskList())
                return json.dumps(
                    {'success': 'true', 'msg': 'Task has been updated successfully.', 'data': render_template('tasklist.html', todos=getTaskList())})
            except Exception as err:
                print(f"There are some issues updating the task-{todo_id}!")
                print("==================")
                print(err)
                print("==================")
                return json.dumps(
                    {'success': 'false', 'msg': 'There are some issues adding the task!!', 'data': form.data, 'errors': form.errors})
        else:
            # flash("", "error")
            print(getTaskList())
            return json.dumps(
                {'success': 'false', 'msg': 'Validation failed.', 'data': form.data, 'errors': form.errors})

    # Mark TODO task by ID
    if request.endpoint == 'markTodo':
        print(f"Mark/Unmark task-{todo_id} as was started....")
        task = Task.query.get_or_404(todo_id)
        checked = request.get_json()
        task.is_done = 1 if checked['check'] else 0
        try:
            db.session.commit()
            print(f"Task-{todo_id} was marked/unmarked successfully.")
            print(getTaskList())
            return json.dumps(
                {'success': 'true', 'msg': 'Task has been updated successfully.', 'data': render_template('tasklist.html', todos=getTaskList())})
        except Exception as err:
            print(f"There are some issues updating the task-{todo_id}!")
            print("==================")
            print(err)
            print("==================")
            return json.dumps(
                {'success': 'false', 'msg': 'There are some issues adding the task!!', 'data': form.data, 'errors': form.errors})

    # Deleting task by ID
    if request.endpoint == 'delete':
        print(f"Delete task-{todo_id} was started....")
        task = Task.query.get_or_404(todo_id)
        print(task.is_done)
        try:
            db.session.delete(task)
            db.session.commit()
            print(f"Task-{todo_id} was deleted successfully.")
            return json.dumps(
                {'success': 'true', 'data': render_template('tasklist.html', todos=getTaskList())})
        except:
            print(f"There are some issues deleting the task-{todo_id}!")
            return "There are some issues deleting the task!"
    return render_template(
        "todo.html",
        todos=todos,
        menu=menu,
        form=form,
        reqMethod=request.method
    )
