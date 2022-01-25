#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : simple_demo.py
# @Author: Lizi
# @Date  : 2020/11/13

import logging
from functools import wraps


# 定义一个装饰器，将函数作为一个参数传给另一个函数
def new_decorator(func_1):
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        print('{}'.format(func_1.__name__))  # 内部函数使用外部函数的变量
        func_1()
        print("I am doing some boring work after executing a_func()")

    return wrapTheFunction  # 此时返回的是一个函数。外部函数返回内部函数，不加()是因为wrapTheFunction()是调用一个函数，而不是返回一个函数


def func():
    print("I am the function which needs some decoration to remove my foul smell")


# 装饰过程
new_func = new_decorator(func)  # 将func函数作为参数赋值给装饰器函数new_decorator。然后将装饰器函数new_decorator的返回值赋值给变量new_func
new_func()  # 因为装饰器返回的是一个函数，因此需要加上()调用该函数
print(new_func.__name__)  # 此时输出的名字为wrapTheFunction，而应该输出func。因为被函数被warpTheFunction替代了。

# ----------------------------------------------------------------------------------------------------------------------


'''以下是使用@ 修饰符调用一个装饰器'''


# 定义一个装饰器，将函数作为一个参数传给另一个函数
def new_decorator(func_1):
    """
    可避免函数名被替代。@wraps接受一个函数来进行装饰，并加入了复制函数名称、注释文档、参数列表等等的功能。
    这可以让我们在装饰器里面访问在装饰之前的函数的属性。
    """

    @wraps(func_1)
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        print('{}'.format(func_1.__name__))
        func_1()  # 内部函数使用外部函数的变量
        print("I am doing some boring work after executing a_func()")

    return wrapTheFunction  # 此时返回的是一个函数，外部函数返回内部函数，不加()是因为wrapTheFunction()是调用一个函数，而不是返回一个函数


@new_decorator
def func():
    print("I am the function which needs some decoration to remove my foul smell")


func()
print(func.__name__)  # 输出func
