# Lab-5 ORM. Modelling with Flask-SQLAlchemy

1. Create model "Task":

|    Task     |                       |
| :---------: | :-------------------: |
|     id      |       int (PK)        |
|    title    |        varchar        |
| description |        varchar        |
|   created   |       timestamp       |
|  priority   | enum(low,medium,high) |
|   is_done   |        boolean        |

Set the created default, priority, is_done fields to the default values,
implement the `__repr__` method in the Task class.

2. Using the command line to initialize the creation of the corresponding table in the SQlite database,
   create some two instances of Task and save them in the database, then get all the records from the database, by making a request.
3. Implement routing and appropriate templates for the Task CRUD model.

| Method | Path                    | Action                |
| ------ | ----------------------- | --------------------- |
| POST   | `/task/create`          | Add a task            |
| GET    | `/task`                 | List all of the tasks |
| GET    | `/task/<int:id>`        | View a task           |
| POST   | `/task/<int:id>/update` | Update a task         |
| POST   | `/task/<int:id>/delete` | Delete a task         |

###### Model Realization

![Model Realization](./screens/model.png)

###### Existing routing

![Existing routing](./screens/routing.png)

###### Database Contents

![Database Contents](./screens/db-contents.png)

###### Starting the Server

![Starting the Server](./screens/start-server.png)

###### Init Screen

![Init Screen](./screens/init-screen.png)

###### Adding new Tasks

![Adding new Tasks](./screens/add-new-1.png)

![Adding new Tasks](./screens/add-new-2.png)

![Adding new Tasks](./screens/add-new-3.png)

![Adding new Tasks](./screens/add-new-4.png)

###### Editing Tasks

![Editing Tasks](./screens/edit-1.png)

![Editing Tasks](./screens/edit-2.png)

###### Deleting Tasks

![Deleting Tasks](./screens/delete-task.png)

###### View Task Data

![View Task Data](./screens/view-task.png)

###### View Task Dates

![View Task Dates](./screens/dates.png)
