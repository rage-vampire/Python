#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : max_divisor.py
# @Author: Lizi
# @Date  : 2020/10/10






def divisor(x, y):
    if x > y:
        smaller = y
    else:
        smaller = x

    for i in range(1, smaller+1):
        if ((x % i == 0) and (y % i == 0)):
            hcf = i
    return hcf

x = int(input('please enter x :'))
y = int(input('please enter y :'))
print('{}和{}最大公约数为：{}'.format(x, y, divisor(x, y)))