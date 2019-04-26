#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/21 12:19
# @Author  : xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : main.py 
# @Software: PyCharm
import os
import time
from . import view
from app import db
from model.car import Car
from sqlalchemy import or_
from hashlib import sha224
from datetime import datetime
from model.admin import Admin
from model.upload import Upload
from flask_login import login_required, current_user, logout_user
from flask import request, render_template, abort, json, redirect


@view.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@view.route('/')
def index():
    return redirect('/login')


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
                if current_user.id == admin.id:
                    logout_user()
                return json.dumps({'code': 200, 'msg': '修改成功'})
            elif o_type == 'destroy':
                _id = request.values.get('id')
                if not _id:
                    return json.dumps({'code': 500, 'msg': '参数错误'})
                admin = Admin.query.get(_id)
                admin.is_alive = False
                db.session.commit()
                if current_user.id == admin.id:
                    logout_user()
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


@view.route('/car_manage', methods=['GET', 'POST'])
@login_required
def car_manage():
    if request.method == 'GET':
        return render_template('car_manage.html')
    else:
        o_type = request.values.get('type')
        if o_type == 'list':
            key_word = request.values.get('key_word')
            page = request.values.get('page', 1)
            limit = request.values.get('limit', 10)
            if key_word:
                _car_list = Car.query.filter(
                    or_(
                        Car.car_type.like(f'%{key_word}%'),
                        Car.car_title.like(f'%{key_word}%'),
                        Car.classification.like(f'%{key_word}%'),
                        Car.car_desc.like(f'%{key_word}%')
                    )
                )
            else:
                _car_list = Car.query

            count = _car_list.count()
            _car_list = _car_list.order_by(
                db.case(
                    (
                        (Car.update_time, Car.update_time),
                    ), else_=Car.build_time
                ).desc()
            ).paginate(int(page), int(limit)).items
            car_list = []
            for item in _car_list:
                car_list.append({
                    'id': item.id,
                    'car_type': item.car_type,
                    'car_title': item.car_title,
                    'classification': item.classification,
                    'city': item.city,
                    'car_left': item.car_left,
                    'status': item.status
                })
            return json.dumps({'code': 200, 'data': car_list, 'count': count})
        elif o_type == 'online':
            _id = request.values.get('id')
            if not _id:
                return json.dumps({'code': 500, 'msg': '参数错误'})
            car = Car.query.get(_id)
            car.status = True
            db.session.commit()
            return json.dumps({'code': 200, 'msg': '上线车辆信息成功'})
        elif o_type == 'destroy':
            _id = request.values.get('id')
            if not _id:
                return json.dumps({'code': 500, 'msg': '参数错误'})
            car = Car.query.get(_id)
            car.status = False
            db.session.commit()
            return json.dumps({'code': 200, 'msg': '下线车辆信息成功'})


@view.route('/car_info', methods=['GET', 'POST'])
@login_required
def car_info():
    if request.method == 'GET':
        _id = request.values.get('id')
        if _id:
            car = Car.query.get(_id)
            if not car:
                abort(404)
            return render_template('car_info.html', car=car)
        else:
            return render_template('car_info.html', car=Car())
    else:
        _args = request.values.to_dict()
        _id = _args.get('id')
        if _id:
            # 修改
            car = Car.query.get(_id)
            car.update_time = datetime.now()
        else:
            # 新增
            car = Car()
            car.status = 'normal'
        car.img = _args.get('img')
        car.car_type = _args.get('car_type')
        car.car_title = _args.get('car_title')
        car.classification = _args.get('classification')
        car.city = _args.get('city')
        car.car_desc = _args.get('car_desc')
        car.car_left = _args.get('car_left')
        car.day_rent_original = _args.get('day_rent_original')
        car.day_rent_actual = _args.get('day_rent_actual')
        car.deposit_original = _args.get('deposit_original')
        car.deposit_actual = _args.get('deposit_actual')
        car.mileage_limit_per_day_original = _args.get('mileage_limit_per_day_original')
        car.mileage_limit_per_day_actual = _args.get('mileage_limit_per_day_actual')
        car.ext_mileage_pay_original = _args.get('ext_mileage_pay_original')
        car.ext_mileage_pay_actual = _args.get('ext_mileage_pay_actual')
        car.ext_time_pay_original = _args.get('ext_time_pay_original')
        car.ext_time_pay_actual = _args.get('ext_time_pay_actual')
        car.month_rent_original = _args.get('month_rent_original')
        car.month_rent_actual = _args.get('month_rent_actual')
        db.session.add(car)
        db.session.commit()
        return json.dumps({'code': 200, 'msg': '保存成功'})


@view.route('/upload', methods=['POST'])
def upload():
    try:
        # 取sha1，判断图片是否已经存在,如果已经存在，则直接返回链接地址，否则写文件，返回地址
        f_name_ori = next(request.files.keys())
        f_byte = request.files.get(f_name_ori).stream._file.read()
        sha224_str = sha224(f_byte).hexdigest()
        upload_info = Upload.query.filter_by(sha224=sha224_str).first()
        if upload_info:
            return json.dumps({'code': 200, 'msg': '', 'data': {'src': f'/static/uploads/{upload_info.path}/{upload_info.file_name}', 'title': upload_info.file_name}})
        else:
            suffix = request.files.get(f_name_ori).filename.split('.')[-1]
            f_name = f"{round(time.time())}.{suffix}"
            _date = datetime.now().strftime('%Y%m%d')
            _path = os.path.join('static', 'uploads', _date)
            if not os.path.exists(_path):
                os.makedirs(_path)
            with open(os.path.join(_path, f_name), 'wb') as f_obj:
                f_obj.write(f_byte)
            u = Upload(path=_date, file_name=f_name, sha224=sha224_str)
            db.session.add(u)
            db.session.commit()
            return json.dumps({'code': 200, 'msg': '', 'data': {'src': f'/static/uploads/{_date}/{f_name}', 'title': f_name}})
    except Exception as e:
        return json.dumps({'code': 500, 'msg': '网络异常，请稍候重试'})


@view.route('/api/car/search', methods=['POST'])
def search():
    car_type = request.values.get('t')
    classification = request.values.get('c')
    min_day_rent = request.values.get('min')
    max_day_rent = request.values.get('max')
    page = request.values.get('p', '1')
    page_limit = request.values.get('limit', '12')
    _car_list = Car.query.filter_by(status=True)
    if car_type:
        _car_list.filter_by(car_type=car_type)
    if classification:
        _car_list.filter_by(classification=classification)
    if min_day_rent:
        _car_list.filter_by(
            or_(
                Car.day_rent_actual > int(min_day_rent),
                not Car.day_rent_actual
            )
        )
    if max_day_rent:
        _car_list.filter_by(
            or_(
                Car.day_rent_actual < int(max_day_rent),
                not Car.day_rent_actual
            )
        )
    count = _car_list.count()
    car_list = _car_list.paginate(int(page), int(page_limit)).items
    return_data = []
    for _ in car_list:
        return_data.append({
            'id': _.id,
            'img': _.img,
            'type': _.car_type,
            'title': _.car_title,
            'city': _.city,
            'rent': _.day_rent_actual if _.day_rent_actual else '面议'
        })
    return json.dumps({'code': 200, 'data': return_data, 'total': count})


@view.route('/api/car/detail', methods=['POST'])
def car_detail():
    _id = request.values.get('id')
    if not _id:
        return json.dumps({'code': 500, 'msg': '参数错误'})
    _car_detail = Car.query.get(_id)
    if not _car_detail:
        return json.dumps({'code': 500, 'msg': '查无此车辆信息'})
    return_data = {
        'id': _car_detail.id,
        'img': _car_detail.img,
        'car_type': _car_detail.car_type,
        'car_title': _car_detail.car_title,
        'classification': _car_detail.classification,
        'city': _car_detail.city,
        'car_desc': _car_detail.car_desc,
        'car_left': _car_detail.car_left,
        'day_rent_original': _car_detail.day_rent_original or '面议',
        'day_rent_actual': _car_detail.day_rent_actual or '面议',
        'deposit_original': _car_detail.deposit_original or '面议',
        'deposit_actual': _car_detail.deposit_actual or '面议',
        'mileage_limit_per_day_original': _car_detail.mileage_limit_per_day_original or '面议',
        'mileage_limit_per_day_actual': _car_detail.mileage_limit_per_day_actual or '面议',
        'ext_mileage_pay_original': _car_detail.ext_mileage_pay_original or '面议',
        'ext_mileage_pay_actual': _car_detail.ext_mileage_pay_actual or '面议',
        'ext_time_pay_original': _car_detail.ext_time_pay_original or '面议',
        'ext_time_pay_actual': _car_detail.ext_time_pay_actual or '面议',
        'month_rent_original': _car_detail.month_rent_original or '面议',
        'month_rent_actual': _car_detail.month_rent_actual or '面议'
    }
    return json.dumps({'code': 200, 'data': return_data})
