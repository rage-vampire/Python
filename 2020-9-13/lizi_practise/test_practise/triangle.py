#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : triangle.py
# @Author: Lizi
# @Date  : 2020/11/3


# 打印三角形
row = 10
for i in range(0, row):
    for k in range(0, row-i):
        # print(k, end='')
        print(' ', end='')   # 先打印空格，每行输出row-i个空格
    for j in range(0, i+1):
        print(' * ', end='')   # 打印*号，end用于
        print(' ', end='')
    # # print('')  # 每打印一行*进行换行




