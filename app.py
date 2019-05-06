#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/21 12:17
# @Author  : xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : app.py
# @Software: PyCharm
import argparse
from flask import Flask
from config import Config
from gevent import monkey
from gevent import pywsgi
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

monkey.patch_socket()

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# 注册蓝图
from view import view

app.register_blueprint(view)

from model.user import User
from model.upload import Upload
from model.car import Car, CarType, Classification

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, required=True, default=9524)
    args = parser.parse_args()
    port = args.port
    server = pywsgi.WSGIServer(('127.0.0.1', port), app)
    server.serve_forever()
