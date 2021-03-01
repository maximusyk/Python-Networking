from flask import Flask
from portfolio import views


def createApp():
    app = Flask(__name__)
    app.config.from_object('config')

    return app
