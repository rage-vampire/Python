#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : parallelogram.py
# @Author: Lizi
# @Date  : 2020/11/4


# 打印平行四边形
row = 5
for i in range(row):
    for k in range(i+1):   # 先打印空格，每行输出i+1个空格
        print('  ', end='')
    for j in range(row+1):
        print(' * ', end='')     # 打印*，每行数出row+1个*
    print('')

for i in range(8):
    if i < 5:
        str = "*" * (i * 2 - 1)
    else:
        str = "*" * (15 - 2 * i)
    print(str.center(7))
