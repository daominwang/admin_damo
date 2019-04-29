#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/21 12:17
# @Author  : xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : login.py 
# @Software: PyCharm
import json
from . import view
from flask import json
from model.user import User
from app import login_manager
from model.form import LoginForm
from flask import request, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('view.login'))


@view.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user_name = form.username.data
            password = form.password.data
            user_list = User.query.filter_by(username=user_name)
            if user_list.count():
                user_info = user_list.first()
                if not user_info.is_alive:
                    return json.dumps({'code': 500, 'msg': '该账号已被禁用'})
                if not user_info.check_password(password):
                    return json.dumps({'code': 500, 'msg': '帐号或密码不正确'})

                login_user(user_info)
                current_user.set_login_time()
                return json.dumps({'code': 200, 'msg': 'success'})
            else:
                return json.dumps({'code': 500, 'msg': '帐号或密码不正确'})
        else:
            return json.dumps({'code': 500, 'msg': '参数错误'})


@view.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('view.login'))
