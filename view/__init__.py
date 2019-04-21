#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/21 10:57
# @Author  : xtmin
# @Email   : wangdaomin123@hotmail.com
# @File    : __init__.py
# @Software: PyCharm
from flask import Blueprint

view = Blueprint('view', __name__)

from .main import *
from .login import *
