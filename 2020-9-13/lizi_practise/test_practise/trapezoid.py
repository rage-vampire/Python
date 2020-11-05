#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : trapezoid.py
# @Author: Lizi
# @Date  : 2020/11/4



# 直角梯形
row = 5
for i in range(row):
    for j in range(row):
        print(' * ', end='')
    for k in range(i+1):
        print(' * ', end='')
    print('')


#等腰梯形
width = 8
num = int(width/2)

for i in range(1, width):
    for k in range(0, width - i):
        print('   ', end='')
    # if i < num:
    #     num_count = (num + (i - 1) * 2)
    print(' * ' * (num+(i-1)*2))