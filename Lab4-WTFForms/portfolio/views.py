import json
import os
import sys
from datetime import date, datetime

from flask import flash, redirect, render_template, request, session, url_for
from flask_mail import Mail, Message

from . import app
from .forms import ContactForm, csrf

mail = Mail()
csrf.init_app(app)
mail.init_app(app)

menu = [("Home", "/", "home"),
        ("About", "/about", "user"),
        ("Portfolio", "/portfolio", "book-content"),
        ("Contact", "/contact", "envelope")]

currDate = date.today()


def writeJSON(data, filename='dump.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


@app.route('/')
@app.route('/hero')
def index():
    session.clear()
    return render_template('index.html', menu=menu, my_os=os.uname(),
                           user_agent=request.headers.get('User-Agent'), version=sys.version,
                           time_now=datetime.now().strftime("%H:%M"))


@app.route('/about')
def about():
    session.clear()
    return render_template('about.html', menu=menu, my_os=os.uname(),
                           user_agent=request.headers.get('User-Agent'), version=sys.version,
                           time_now=datetime.now().strftime("%H:%M"))


@app.route('/portfolio')
def portfolio():
    session.clear()
    return render_template('portfolio.html', menu=menu, my_os=os.uname(),
                           user_agent=request.headers.get('User-Agent'), version=sys.version,
                           time_now=datetime.now().strftime("%H:%M"))


@ app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    isValidName = ""
    isValidEmail = ""
    isValidSubject = ""
    isValidMessage = ""
    if request.method == 'POST':
        if 'name' in session and 'email' in session:
            print(f"Name -> {session.get('name')}\nEmail -> {session.get('email')}")
            form.name.data = session.get('name')
            form.email.data = session.get('email')
            if form.validate_on_submit():
                sbj = request.form['subject']
                msg = request.form['message']
                with open('dump.json') as jsonFile:
                    data = json.load(jsonFile)
                    temp=data['usrMessages']
                    temp.append({'Name': form.name.data, 'Email': form.email.data, 'Subject': form.subject.data, 'Message': form.message.data})
                writeJSON(data)
                flash(u'Your message has been sent. Thank you!', 'message')
                return redirect(url_for('contact'))
            else:
                flash(u'There were some issues sending the message!', 'error')
        else:
            if form.validate_on_submit():
                usrName = form.name.data
                usrEmail = form.email.data
                sbj = form.subject.data
                msg = form.message.data
                session['name']=usrName
                session['email']=usrEmail
                with open('dump.json') as jsonFile:
                    data = json.load(jsonFile)
                    temp=data['usrMessages']
                    temp.append({'Name': form.name.data, 'Email': form.email.data, 'Subject': form.subject.data, 'Message': form.message.data})
                writeJSON(data)
                flash(u'Your message has been sent. Thank you!', 'message')
                return redirect(url_for('contact'))
            else:
                flash(u'There were some issues sending the message!', 'error')
    return render_template('contact.html',
                           menu=menu,
                           form=form,
                           usrName=session.get('name'),
                           usrEmail=session.get('email'),
                           isValidName=isValidName,
                           isValidEmail=isValidEmail,
                           isValidSubject=isValidSubject,
                           isValidMessage=isValidMessage,
                           my_os=os.uname(),
                           user_agent=request.headers.get('User-Agent'),
                           version=sys.version,
                           time_now=datetime.now().strftime("%H:%M"))
