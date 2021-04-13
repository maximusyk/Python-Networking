# Lab-7 UserSystem+Blueprints

1. Refactor project to work with Blueprints.
2. Add Registration and Login forms and models.
3. Make routes to work with forms and models.
4. Validate forms(Registration: check if user exist, email, password match; Login: check if user exist, password match with db).

###### Project Structure

![project-structure](./screens/project-structure.png)

###### Example of `__init__.py` file with Blueprint

```__init__.py
from flask import Blueprint


users_bp = Blueprint('users_bp', __name__, template_folder="templates/users")

```

###### Example of view file with Blueprint

![blue-view](./screens/blue-view.png)

###### Sign up form

![Sign up form](./screens/sign-up-form.png)

###### Sign up form validation overlook

![up-empty-val](./screens/up-empty-val.png)

![up-val-design](./screens/up-val-design.png)

![up-name-val](./screens/up-name-val.png)

![up-email-val](./screens/up-email-val.png)

![up-pwd-val](./screens/up-pwd-val.png)

![up-conpwd-val](./screens/up-conpwd-val.png)

![up-success](./screens/up-success.png)

###### Sign in form

![sign-in-form](./screens/sign-in-form.png)

###### Sign up form validation overlook

![in-val-design](./screens/in-val-design.png)

![in-name-val](./screens/in-name-val.png)

![in-pwd-val](./screens/in-pwd-val.png)

![in-success](./screens/in-success.png)
