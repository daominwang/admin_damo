#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/21 22:38
# @Author  : xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : config.py 
# @Software: PyCharm
import os


class Config(object):
    SECRET_KEY = 'UNj^SlGYg24eWb&MoVQ*D34a7#zI6EWD'
    basedir = os.path.abspath(os.path.dirname(__file__))

    USERNAME = 'car'
    PASSWORD = 'ZXU7CI@WZht3RqVq'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'car_rent'

    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:{}/{}?charset=utf8'.format(
        USERNAME, PASSWORD, HOST, PORT, DATABASE
    )

    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 30
    SQLALCHEMY_MAX_OVERFLOW = 20
