#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/21 12:36
# @Author  : xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : form.py 
# @Software: PyCharm
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField(label='用户名', validators=[DataRequired('请输入用户名')])
    password = PasswordField(label='密码', validators=[DataRequired('请输入密码')])
    submit = SubmitField(label='submit')

    def validate_username(self, field):
        # 验证用户名是否重复
        return True

    def validate_password(self, field):
        # 验证用户名是否重复
        return True
