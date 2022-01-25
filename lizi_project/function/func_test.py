#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : func_test.py
# @Author: Lizi
# @Date  : 2020/9/13


def add(x,y,z):
    return x+y+z


params = (1,2,3)
print(add(*params))


def hello(name='yanglili',greeting='hello'):
    '''**将字典中的值分配给关键字参数'''
    print("{},{}".format(greeting,name))


params = {'name':'123', "greeting":'well meeting'}
hello(**params)



def fun_globals(param):
    '''globals()函数指定全局变量'''
    extent = '123'
    print(param + extent)  # 使用局部变量
    print(param+globals()['extent'])  # 使用全局变量

extent = 'berry'
fun_globals('Sub')


x = 1
def change_global():
    global x    # 默认为局部变量，使用global指定为全局变量
    x += 1
    print(x)

change_global()