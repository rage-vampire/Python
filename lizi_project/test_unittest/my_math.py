#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : my_math.py
# @Author: Lizi
# @Date  : 2020/11/2


import math


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def multi(a, b):
    return a * b


def div(a, b):
    if b == 0:
        raise ValueError("除数为0")
    else:
        return a / b


def sqrt(a):
    if a < 0:
        raise ValueError("invalid value:{0}".format(a))
    else:
        return math.sqrt(a)


def f():
    raise SystemError(0)


