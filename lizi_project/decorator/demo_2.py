#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : demo_2.py
# @Author: Lizi
# @Date  : 2020/11/13

from functools import wraps

'''被装饰的函数带有参数'''
can_run = True
def decorator_name(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not can_run:
            return 'Function will not run'
        return func(*args, **kwargs)   # 调用函数func()，并返回func()的值
    return decorated


@decorator_name
def func_1():
    return 'Functiong is running'

# can_run = False
res = func_1()
print(res)
print(func_1.__name__)