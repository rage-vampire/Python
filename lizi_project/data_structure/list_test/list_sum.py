#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : list_sum.py
# @Author: Lizi
# @Date  : 2020/10/12


'''计算列表之和'''
'''实例1'''
def sum_add(list):
    total = 0
    for i in list:
        total += i
    print(total)


'''实例2,使用while循环'''
def sum_add2(list):
    total = 0
    ele = 0
    while ele < len(list):
        total += list[ele]
        ele += 1
    print(total)


li = [11, 22, 33, 44]
sum_add(li)
sum_add2(li)



'''实例3，使用递归'''
list1 = [11, 5, 17, 18, 23]
def sumOfList(list, size):
    if (size == 0):
        return 0
    else:
        return list[size - 1] + sumOfList(list, size - 1)

total = sumOfList(list1, len(list1))

print("列表元素之和为: ", total)
