# coding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin
from flask_bootstrap import Bootstrap


class Anonymous(AnonymousUserMixin):
    """
    匿名用户类 增加id与nickname属性，用于判断
    """
    def __init__(self):
        self.id = 9999
        self.nickname = 'Guest'


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.anonymous_user = Anonymous   # 指定匿名用户类
bs = Bootstrap(app)

from app import views, models

