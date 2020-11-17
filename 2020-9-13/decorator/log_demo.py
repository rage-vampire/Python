#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : log_demo.py
# @Author: Lizi
# @Date  : 2020/11/13

from functools import wraps
import logging

'''
    装饰器本质上也是一个函数或类，它可以让其他函数或者类在不需要做任何代码修改的前提下增加额外功能，装饰器的返回值是一个函数或者类。
    理解装饰器的前提：
    1、一切皆对象（函数可以当做对象传递）
    2、闭包
        1、函数的嵌套
        2、内部函数使用外部函数的变量
        3、外部函数的返回值为内部函数
'''

'''实例1：被装饰的函数带有参数'''


def log(func):  # func---->addidtion_func()
    @wraps(func)
    def with_logging(*args, **kwargs):  # 被装饰的函数带有参数
        print(func.__name__ + ' was called')
        return func(*args, **kwargs)  # 返回值--->addition_func()

    return with_logging  # with_logging = addittion_func()


@log
def addition_func(x):
    return x * x


result = addition_func(3)
print(result)
# ----------------------------------------------------------------------------------------------------------------------

'''实例2：装饰器自身带有参数'''


def log_level(level):
    def log(func):
        @wraps(func)
        def with_logging(*args, **kwargs):
            if level == 'warning':
                logging.warning(func.__name__ + ' was called')
                return func(*args, **kwargs)
            elif level == 'error':
                logging.error(func.__name__ + ' was called')
                return func(*args, **kwargs)

        return with_logging

    return log


@log_level('warning')
def func1():
    print('func1')


@log_level('error')
def func2():
    print('func2')


func1()
func2()
