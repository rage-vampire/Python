#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : inset_sort.py
# @Author: Lizi
# @Date  : 2020/10/14

'''插入排序'''

def insert_sort(arr):
    for i in range(1, len(arr)):

        if arr[i-1] > arr[i]:
            arr[i-1], arr[i] = arr[i], arr[i-1]
            for j in range(i):
                return insert_sort(arr)
    return arr

arr = [10, 6, 2, 8, 77, 33, 22, 9, 55, 9, 5, 4, 3]
print(insert_sort(arr))