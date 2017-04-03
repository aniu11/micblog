# coding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.id = 9999
        self.nickname = 'Guest'

    def is_anonymous(self):
        return True

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.anonymous_user = Anonymous

from app import views, models

