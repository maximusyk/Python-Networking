# region IMPORTS
import json
from functools import wraps

from app.users import users_bp
from flask import g, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .forms import *
from .models import *

# endregion


# region CUSTOM_DEC
def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('home_bp.index', next=request.url) + '&auth_req')
        return f(*args, **kwargs)
    return decorated_function
# endregion


# region _VARS
menu = [
    ("User", "/register", "user"),
    ("Home", "/", "home"),
    ("About", "/about", "info-circle"),
    ("Portfolio", "/portfolio", "book-content"),
    ("Contact", "/contact", "envelope"),
    ("ToDo List", "/todo", "list-check"),
]
# endregion


# region PORTFOLIO
@users_bp.route("/signup", methods=["GET", "POST"], endpoint='register')
@users_bp.route("/signin", methods=["GET", "POST"], endpoint='login')
@users_bp.route("/user_form", methods=["GET"], endpoint='user_form')
def users():
    form_up = RegistrationForm()
    form_in = LoginForm()
    users = User.query.all()

    if request.endpoint == 'users_bp.register':
        if current_user.is_authenticated:
            return redirect(url_for('users_bp.account'))
        if form_up.validate_on_submit():
            usrname = request.form['username']
            email = request.form['email_up']
            pwd = request.form['password_up']
            errors = {}

            for usr in users:
                if usrname == usr.username:
                    errors["username"] = ["Username already taken"]
                else:
                    if "username" in form_up.errors:
                        errors["username"] = form_up.errors["username"]

                if email == usr.email:
                    errors["email_up"] = ["Email already taken"]
                else:
                    if "email_up" in form_up.errors:
                        errors["email_up"] = form_up.errors["email_up"]

            if "email_up" in errors or "password_up" in errors:
                return json.dumps({
                    "success": "BAD",
                    "errors": "User exist",
                    "data": form_up.data
                })

            user = User(username=usrname, email=email, password=pwd)
            try:
                db.session.add(user)
                db.session.commit()

                return json.dumps({
                    "success": "OK",
                    "Title": "User successfuly registered"
                })
            except Exception as e:
                json.dump({
                    "success": "BAD",
                    "Title": "There are some issues adding the user",
                    "errors": e
                })
        else:
            # usrname = request.form['username']
            # email = request.form['email_up']
            return json.dumps({"success": "BAD", "data": form_up.data,
                               "errors": form_up.errors})

    if request.endpoint == 'users_bp.login':
        if current_user.is_authenticated:
            return redirect(url_for('users_bp.account'))
        if form_in.validate_on_submit():
            email = request.form['email_in']
            pwd = request.form['password_in']
            errors = {
                "email_in": "",
                "password_in": "",
            }
            user_db = User.query.filter_by(email=email).first()
            if not user_db:
                user_db = User.query.filter_by(username=email).first()
            if user_db:
                del errors["email_in"]
                if user_db.verify_password(pwd):
                    del errors["password_in"]
                else:
                    errors["password_in"] = ["Wrong password"]
            else:
                errors["email_in"] = ["Username or email not found"]
                errors["password_in"] = ["Wrong password"]

            if "email_in" in errors or "password_in" in errors:
                return json.dumps({
                    "success": "BAD",
                    "errors": errors,
                    "data": form_in.data
                })

            login_user(user_db, remember=form_in.remember_me.data)
            # TODO move nav menu to helpers
            return json.dumps({
                "success": "OK",
                "data": render_template("nav_menu.html", menu=menu)
            })
        else:
            email = request.form['email_in']
            pwd = request.form['password_in']
            errors = {
                "email_in": "",
                "password_in": "",
            }
            user_db = User.query.filter_by(email=email).first()
            if not user_db:
                user_db = User.query.filter_by(username=email).first()
            if user_db:
                del errors["email_in"]
                if user_db.verify_password(pwd):
                    del errors["password_in"]
                else:
                    errors["password_in"] = ["Wrong password"]
            else:
                errors["email_in"] = ["Username or email not found"]
                errors["password_in"] = ["Wrong password"]

            if "email_in" in errors or "password_in" in errors:
                return json.dumps({
                    "success": "BAD",
                    "errors": errors,
                    "data": form_in.data
                })
            return json.dumps({"success": "BAD", "data": form_in.data,
                               "errors": form_in.errors})

    return json.dumps({
        "data": render_template("user_form.html", form_up=form_up, form_in=form_in, req_method=request.method)
    })
# endregion


@users_bp.route("/logout", methods=["GET"])
@auth_required
def logout():
    logout_user()
    return redirect(url_for('home_bp.index'))


@users_bp.route("/account", methods=["GET"])
@auth_required
def account():
    return render_template("account.html", menu=menu)
