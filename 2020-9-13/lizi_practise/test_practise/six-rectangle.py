#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : six-rectangle.py
# @Author: Lizi
# @Date  : 2020/11/4

# row = 6
# for i in range(row):
#     for k in range(0, row-i):
#         print('   ', end='')
#     for j in range(i+1):
#         print(' * ', end='')
#     for n in range(row-2):
#         print(' * ', end='')
#     for m in range(i+1):
#         print(' * ', end='')
#     print('')
#
# for i in range(row-1):
#     for k in range(i+2):   # 先打印空格，每行输出i+1个空格
#         print('   ', end='')
#     for j in range(row-i):
#         print(' * ', end='')     # 打印*，每行数出row-i个*
#     for n in range(row-3):
#         print(' * ', end='')
#     for m in range(row-i-1):
#         print(' * ', end='')
#     print('')


width = 8
num = int(width/2)

for i in range(1, width):
    for k in range(0, width - i):
        print('   ', end='')
    if i < num:
        num_count = (num + (i - 1) * 2)
        print(' * ' * (num+(i-1)*2))



