#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : cube_sum.py
# @Author: Lizi
# @Date  : 2020/10/10


'''计算n个数的立方和'''
sum = 0
n = int(input('please enter num :'))
for i in range(n+1):
    sum += i ** 3
print('{}的立方和为：{}'.format(n, sum))