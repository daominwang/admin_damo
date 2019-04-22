#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/21 12:36
# @Author  : xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : form.py 
# @Software: PyCharm
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    username = StringField(label='用户名', validators=[DataRequired('请输入用户名')])
    password = PasswordField(label='密码', validators=[DataRequired('请输入密码')])
    submit = SubmitField(label='提交')
