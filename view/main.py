#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/21 12:19
# @Author  : xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : main.py 
# @Software: PyCharm
from . import view
from model.admin import Admin
from flask_login import login_required
from flask import request, render_template, abort, json, jsonify


@view.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@view.route('/')
@login_required
def index():
    return render_template('index.html')


@view.route('/user/<user_type>', methods=['GET', 'POST'])
@login_required
def user_manage(user_type):
    if user_type == 'admin':
        if request.method == 'POST':
            page = request.values.get('page', 1)
            limit = request.values.get('limit', 10)
            _admin_list = Admin.query.order_by(Admin.last_login_time.desc()).paginate(int(page), int(limit)).items
            admin_list = []
            for item in _admin_list:
                admin_list.append({
                    'id': item.id,
                    'username': item.username,
                    'is_alive': item.is_alive,
                    'last_login_time': item.last_login_time.strftime('%Y-%m-%d %H:%M:%S') if item.last_login_time else None
                })
            return json.dumps({'code': 200, 'data': admin_list})
    elif user_type == 'user':
        pass
    else:
        abort(404)
    return render_template('user_manage.html', user_type=user_type)


@view.route('/car', methods=['GET', 'POST'])
@login_required
def car_manage():
    if request.method == 'GET':
        return render_template('car_manage.html')
    else:
        pass
