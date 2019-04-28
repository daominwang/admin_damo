#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/21 10:56
# @Author  : xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : user.py
# @Software: PyCharm
from app import db
from datetime import datetime
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    is_alive = db.Column(db.Boolean, nullable=True, default=True)
    is_super = db.Column(db.Boolean, nullable=True, default=False)
    build_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    last_login_time = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def set_login_time():
        current_user.last_login_time = datetime.now()
        db.session.add(current_user)
        db.session.commit()

    def __repr__(self):
        return f'<User {self.username}>'
