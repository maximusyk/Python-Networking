from flask import Flask, redirect, url_for, render_template, request
from datetime import datetime, date
import sys
import os


app = Flask(__name__)
app.config.from_object('config')

menu = [("Home", "/", "home"),
        ("About", "/about", "user"),
        ("Portfolio", "/portfolio", "book-content"),
        ("Contact", "/contact", "envelope")]

currDate = date.today()


@ app.route('/')
@ app.route('/hero')
def index():
    return render_template('index.html', menu=menu, my_os=os.uname(),
                           user_agent=request.headers.get('User-Agent'), version=sys.version,
                           time_now=datetime.now().strftime("%H:%M"))


@ app.route('/about')
def about():
    return render_template('about.html', menu=menu, my_os=os.uname(),
                           user_agent=request.headers.get('User-Agent'), version=sys.version,
                           time_now=datetime.now().strftime("%H:%M"))


@ app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', menu=menu, my_os=os.uname(),
                           user_agent=request.headers.get('User-Agent'), version=sys.version,
                           time_now=datetime.now().strftime("%H:%M"))


@ app.route('/contact')
def contact():
    return render_template('contact.html', menu=menu, my_os=os.uname(),
                           user_agent=request.headers.get('User-Agent'), version=sys.version,
                           time_now=datetime.now().strftime("%H:%M"))


if __name__ == '__main__':
    app.run()
