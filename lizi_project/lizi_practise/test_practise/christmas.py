#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : christmas.py
# @Author: Lizi
# @Date  : 2020/11/4

# 圣诞树
row1 = 5
row2 = 7
row3 = 10
count = 0
for i in range(0, row1):
    for k in range(0, row3-i):
        print('  ', end='')   # 先打印空格，每行数出row-i个空格
    for j in range(0, i+1):
        print(' * ', end='')   # 打印*号，end用于
        print(' ', end='')
    print('')  # 每打印一行*进行换行

for i in range(0, row2):
    for k in range(0, row3-i):
        print('  ', end='')   # 先打印空格，每行数出row-i个空格
    for j in range(0, i+1):
        print(' * ', end='')   # 打印*号，end用于
        print(' ', end='')
    print('')  # 每打印一行*进行换行
#
# for i in range(0, row3):
#     for k in range(0, row3-i):
#         print('  ', end='')   # 先打印空格，每行数出row-i个空格
#     for j in range(0, i+1):
#         print(' * ', end='')   # 打印*号，end用于
#         print(' ', end='')
#     print('')  # 每打印一行*进行换行
#
# for i in range(7):
#     for j in range(15):
#         print(' ', end='')
#     for k in range(4):
#         print(' * ',end='')
#     print('')
