#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/23 11:11
# @Author  : Xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : car.py
# @Software: PyCharm
from app import db
from datetime import datetime


class Car(db.Model):
    __tablename__ = 'car'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img = db.Column(db.String(64))
    car_type = db.Column(db.String(64))
    car_title = db.Column(db.String(64))
    classification = db.Column(db.String(64))
    city = db.Column(db.String(32))
    car_desc = db.Column(db.Text, nullable=True)
    car_left = db.Column(db.Integer, default=0)
    day_rent_original = db.Column(db.Integer, default=0)
    day_rent_actual = db.Column(db.Integer, default=0)
    deposit_original = db.Column(db.Integer, default=0)
    deposit_actual = db.Column(db.Integer, default=0)
    mileage_limit_per_day_original = db.Column(db.Integer, default=0)
    mileage_limit_per_day_actual = db.Column(db.Integer, default=0)
    ext_mileage_pay_original = db.Column(db.Integer, default=0)
    ext_mileage_pay_actual = db.Column(db.Integer, default=0)
    ext_time_pay_original = db.Column(db.Integer, default=0)
    ext_time_pay_actual = db.Column(db.Integer, default=0)
    month_rent_original = db.Column(db.Integer, default=0)
    month_rent_actual = db.Column(db.Integer, default=0)
    create_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    build_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    status = db.Column(db.Boolean, nullable=True, default=True)


class CarType(db.Model):
    __tablename__ = 'car_type'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    car_type = db.Column(db.String(64))
    create_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    build_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    status = db.Column(db.Boolean, nullable=True, default=True)


class Classification(db.Model):
    __tablename__ = 'classification'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classification = db.Column(db.String(64))
    create_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    build_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    status = db.Column(db.Boolean, nullable=True, default=True)
