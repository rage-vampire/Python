# -*- coding:utf-8 -*-
# @Filename : function_demo.py
# @Author : Lizi
# @Time : 2020/3/9 10:41 
# @Software: PyCharm

import math


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def multi(a, b):
    return a * b


def div(a, b):
    if b == 0:
        raise ValueError("invalid value:0")
    return a / b


def sqrt(a):
    if a < 0:
        raise ValueError("invalid value:{0}".format(a))
    else:
        return math.sqrt(a)