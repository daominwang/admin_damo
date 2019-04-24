#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/25 00:17
# @Author  : xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : upload.py 
# @Software: PyCharm
from app import db


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(16))
    file_name = db.Column(db.String(64))
    sha224 = db.Column(db.String(128), unique=True)
