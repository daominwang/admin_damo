#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/21 22:38
# @Author  : xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : config.py 
# @Software: PyCharm
import os


class Config(object):
    SECRET_KEY = 'secret'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
