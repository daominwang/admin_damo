#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/21 12:17
# @Author  : xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : login.py 
# @Software: PyCharm
import json
from . import view
from flask import jsonify, json
from model.form import LoginForm
from flask import request, render_template


@view.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            return json.dumps({'code': 200, 'msg': '登陆成功'})
        else:
            return json.dumps({'code': 500, 'msg': '参数错误'})
