# region IMPORTS
import json
import math
import os
import secrets
from datetime import datetime, timedelta
from PIL import Image, ImageOps
from app.users import users_bp
from flask import redirect, render_template, request, url_for, current_app
from flask_login import current_user, login_required, login_user, logout_user

from .forms import *
from .models import *

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


def save_picture(form_pictute):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pictute.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/img/profile_pics', picture_fn)

    img = Image.open(form_pictute)
    img_w, img_h = img.size
    if img_w < 500 or img_h < 500:
        if img_w > img_h:
            output_size = (img_h, img_h)
            img = ImageOps.fit(img, output_size, Image.ANTIALIAS)
        else:
            output_size = (img_w, img_w)
            img = ImageOps.fit(img, output_size, Image.ANTIALIAS)
    else:
        output_size = (500, 500)
        img = ImageOps.fit(img, output_size, Image.ANTIALIAS)

    img.save(picture_path)

    return picture_fn


# region PORTFOLIO


@users_bp.route("/signup", methods=["GET", "POST"], endpoint='register')
@users_bp.route("/signin", methods=["GET", "POST"], endpoint='login')
@users_bp.route("/user/<int:user_id>/get", methods=["GET", "POST"], endpoint='user_get')
@users_bp.route("/user/<int:user_id>/edit", methods=["GET", "POST"], endpoint='user_edit')
@users_bp.route("/user/<int:user_id>/password/change", methods=["GET", "POST"], endpoint='user_pass')
@users_bp.route("/user_form", methods=["GET"], endpoint='user_form')
def users(user_id=None):
    form_up = RegistrationForm()
    form_in = LoginForm()
    form_edit = UserUpdateForm()
    form_pass = ChangePasswordForm()

    users = User.query.all()

    if request.endpoint == 'users_bp.user_get':
        user = User.query.get_or_404(user_id)
        return json.dumps({
            'name': user.username,
            'email': user.email,
            'description': user.description,
            'data': render_template("edit_form.html", form_edit=form_edit, form_pass=form_pass, req_method=request.method)
        })

    if request.endpoint == 'users_bp.user_form':
        if not current_user.is_authenticated:
            return json.dumps({
                "success": "OK",
                "data": render_template("user_form.html", form_up=form_up, form_in=form_in, req_method=request.method)
            })
        else:
            return json.dumps({"success": "AUTH"})

    if request.endpoint == 'users_bp.user_edit':
        if current_user.is_authenticated:
            return redirect(url_for('home_bp.index'))
        else:
            user = User.query.get_or_404(user_id)
            if form_edit.validate_on_submit() and request.method == 'POST':
                if form_edit.picture.data:
                    picture_file = save_picture(form_edit.picture.data)
                    current_user.image_file = picture_file

                current_user.username = request.form['username']
                current_user.email = request.form['email']
                current_user.description = request.form['description']
                db.session.commit()

                return json.dumps({
                    "success": "OK",
                    "Title": "User info successfuly updated"
                })

            else:
                return json.dumps({"success": "BAD", "data": form_edit.data,
                                   "errors": form_edit.errors})

    if request.endpoint == 'users_bp.user_pass':
        if current_user.is_authenticated:
            return redirect(url_for('home_bp.index'))
        else:
            user = User.query.get_or_404(user_id)
            if form_pass.validate_on_submit() and request.method == 'POST':
                old_pwd = request.form['old_pwd']
                if not user.verify_password(old_pwd):
                    form_pass.errors['old_pwd'] = ["Wrong password"]
                    return json.dumps({
                        "success": "BAD",
                        "errors": form_pass.errors,
                        "data": form_pass.data
                    })

                current_user.password = pbkdf2_sha256.hash(
                    request.form['new_pwd'])
                db.session.commit()

                return json.dumps({
                    "success": "OK"
                })
            else:
                old_pwd = request.form['old_pwd']
                errors = form_pass.errors
                if not user.verify_password(old_pwd):
                    print("=====")
                    errors['old_pwd'] = ["Wrong password"]
                print(errors)

                return json.dumps({"success": "BAD", "data": form_pass.data,
                                   "errors": errors})

    if request.endpoint == 'users_bp.register':
        if current_user.is_authenticated:
            return redirect(url_for('home_bp.index'))
        else:
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
            return redirect(url_for('home_bp.index'))
        else:
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
                user_db.last_seen = datetime.now().strftime('%d/%m/%y %H:%M:%S')
                db.session.commit()
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
# endregion


@ users_bp.route("/logout", methods=["GET"])
@ login_required
def logout():
    logout_user()
    # return json.dumps({
    #     "success": "OK"
    # })
    return redirect(url_for('home_bp.index'))


@ users_bp.route("/account", methods=["GET"])
@ login_required
def account():
    image_file = url_for(
        'static', filename='img/profile_pics/' + current_user.image_file)

    last_seen = datetime.strptime(current_user.last_seen, '%d/%m/%y %H:%M:%S')
    time_now = datetime.now()
    time_sec = (time_now - last_seen).total_seconds()
    last_seen = time_sec/60
    if last_seen >= 60:
        last_seen = str(math.floor(last_seen/60))+"h ago"
    else:
        last_seen = math.floor(last_seen)
        if last_seen <= 5:
            last_seen = 'recently'
        else:
            last_seen = str(last_seen)+"m ago"
    return render_template("account.html", menu=menu, last_seen=last_seen, image_file=image_file)
