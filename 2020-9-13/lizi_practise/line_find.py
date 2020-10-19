#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : line_find.py
# @Author: Lizi
# @Date  : 2020/10/13

'''线性查找指按一定的顺序检查数组中每一个元素，直到找到所要寻找的特定值为止。'''

def line_find(arr,x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i, arr[i]
        else:
            continue
            # print(x, '不存在')

arr = [1, 2, 3, 4, 'd']
x = 'd'
print(line_find(arr, x))