#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : dict_sum.py
# @Author: Lizi
# @Date  : 2020/10/13

def sum_value(mydict):
    sum = 0
    for i in key_dict.values():
        sum += i
    return sum


key_dict = {'a': 1, 'b': 2, 'd': 4, 'c': 3}
Sum = sum_value(key_dict)
print('字典值的和为：{}'.format(Sum))