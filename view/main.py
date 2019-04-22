#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/21 12:19
# @Author  : xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : main.py 
# @Software: PyCharm
from . import view
from app import db
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
            o_type = request.values.get('type')
            if o_type == 'list':
                key_word = request.values.get('key_word')
                page = request.values.get('page', 1)
                limit = request.values.get('limit', 10)
                if key_word:
                    _admin_list = Admin.query.filter(Admin.username.like(f'%{key_word}%'))
                else:
                    _admin_list = Admin.query
                _admin_list = _admin_list.order_by(Admin.last_login_time.desc()).paginate(int(page), int(limit)).items
                admin_list = []
                for item in _admin_list:
                    admin_list.append({
                        'id': item.id,
                        'username': item.username,
                        'is_alive': item.is_alive,
                        'last_login_time': item.last_login_time.strftime('%Y-%m-%d %H:%M:%S') if item.last_login_time else None
                    })
                return json.dumps({'code': 200, 'data': admin_list, 'count': Admin.query.count()})
            elif o_type == 'modify':
                _id = request.values.get('id')
                user_name = request.values.get('username')
                if not _id or not user_name:
                    return json.dumps({'code': 500, 'msg': '参数错误'})
                admin = Admin.query.get(_id)
                if not admin:
                    return json.dumps({'code': 500, 'msg': '网络异常，请稍候重试'})
                admin.username = user_name
                db.session.commit()
                return json.dumps({'code': 200, 'msg': '修改成功'})
            elif o_type == 'destroy':
                _id = request.values.get('id')
                if not _id:
                    return json.dumps({'code': 500, 'msg': '参数错误'})
                admin = Admin.query.get(_id)
                admin.is_alive = False
                db.session.commit()
                return json.dumps({'code': 200, 'msg': '删除账号成功'})
            elif o_type == 'online':
                _id = request.values.get('id')
                if not _id:
                    return json.dumps({'code': 500, 'msg': '参数错误'})
                admin = Admin.query.get(_id)
                admin.is_alive = True
                db.session.commit()
                return json.dumps({'code': 200, 'msg': '恢复账号成功'})
            elif o_type == 'add':
                user_name = request.values.get('username')
                password = request.values.get('password')
                if not user_name or not password:
                    return json.dumps({'code': 500, 'msg': '参数错误'})
                admin = Admin()
                admin.username = user_name
                admin.set_password(password)
                db.session.add(admin)
                db.session.commit()
                return json.dumps({'code': 200, 'msg': '添加成功'})
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
