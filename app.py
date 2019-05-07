#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/21 12:17
# @Author  : xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : app.py
# @Software: PyCharm
import argparse
from config import Config
from gevent import monkey
from gevent import pywsgi
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for

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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('view.login'))


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
