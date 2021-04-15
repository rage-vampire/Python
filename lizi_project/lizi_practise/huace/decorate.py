#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : decorate.py
# @Author: Lizi
# @Date  : 2020/11/16

from datetime import datetime
import time

def log_time(func):
    def wrapper(*args,**kwargs):
        print('{}函数开始被执行'.format(func.__name__))
        s_time = datetime.now()
        print('{}函数执行开始时间为：{}'.format(func.__name__, s_time))
        res = func(*args,**kwargs)
        e_time = datetime.now()
        print('{}函数执行消耗时间为：{}'.format(func.__name__, (e_time-s_time)))
        return res
    return wrapper

@log_time
def add(x):
    # time.sleep(2)
    # print('函数执行时间为：{}'.format(datetime_test.now()))
    return x**2

@log_time
def add_sum(num):
    sum = 0
    for i in range(num):
        sum += i
    print(sum)

add(3)
add_sum(10000)