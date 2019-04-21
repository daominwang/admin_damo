#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/21 10:56
# @Author  : xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : user.py 
# @Software: PyCharm
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
