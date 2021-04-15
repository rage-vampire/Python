#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : pai_lie_zuhe.py
# @Author: Lizi
# @Date  : 2020/9/7


# 有四个数字：1、2、3、4，能组成多少个互不相同且无重复数字的三位数？各是多少？
sum = 0
for x in range(1,5):
    for y in range(1,5):
        for z in range(1,5):
            if (x != y) and (x!= z) and (y != z):
                print(x,y,z)
                sum += 1
print('总共有{}个值'.format(sum))