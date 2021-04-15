#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : sort.py
# @Author: Lizi
# @Date  : 2020/9/7
'''输入三个整数x,y,z，请把这三个数由小到大输出。'''
list1 = []
for i in range(3):
    x = int(input("请输入3个数："))
    list1.append(x)
list1.sort()
print(list1)