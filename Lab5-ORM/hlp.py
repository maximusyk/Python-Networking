@app.route("/todo", methods=["GET", "POST"])
@app.route("/todo/<int:todo_id>/getById", methods=["GET", "POST"], endpoint='getById')
@app.route("/todo/<int:todo_id>", methods=["GET", "POST"], endpoint='view')
@app.route("/todo/<int:todo_id>/update", methods=["GET", "POST"], endpoint='update')
@app.route("/todo/<int:todo_id>/delete", methods=["GET", "POST"], endpoint='delete')
def todo(todo_id=None):
    # Index page allows to add new tasks, see these tasks, edit and deleted them.
    form = TaskForm()
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
        todos = [highList, mediumList, lowList, doneList]
    else:
        todos = ''
    # Get data from db by Id
    if request.endpoint == 'getById':
        task = Task.query.get_or_404(todo_id)
        print("<<<==== GET BY ID ====>>>")
        return json.dumps({
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'created_at': task.created_at,
            'deadline': task.deadline,
            'is_done': task.is_done
        })
    # Add new task
    if request.method == "POST":
        if form.validate_on_submit():
            print(request.form['timeline'].split(" - ")[0],
                  request.form['timeline'].split(" - ")[1])
            task = Task(title=request.form['title'], description=request.form['description'],
                        priority=request.form['priority'], created_at=request.form['timeline'].split(" - ")[0], deadline=request.form['timeline'].split(" - ")[1])
            try:
                db.session.add(task)
                db.session.commit()
                return json.dumps(
                    {'success': 'true', 'msg': 'Task has been added successfully.', 'data': form.data})
            except Exception as err:
                db.session.rollback()
                # flash("There are some issues adding the task!!", "error")
                print(err)
                return json.dumps(
                    {'success': 'false', 'msg': 'There are some issues adding the task!!', 'data': form.data, 'errors': form.errors})
        else:
            # flash("", "error")
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
            task.is_done = request.form['is_done']
            try:
                db.session.commit()
                print(f"Task-{todo_id} was updated successfully.")
                return redirect('/todo')
            except:
                print(f"There are some issues updating the task-{todo_id}!")
                return "There are some issues updating the task!"
    # Deleting task by ID
    if request.endpoint == 'delete':
        print(f"Delete task-{todo_id} was started....")
        task = Task.query.get_or_404(todo_id)
        try:
            db.session.delete(task)
            db.session.commit()
            print(f"Task-{todo_id} was deleted successfully.")
            return redirect('/todo')
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
