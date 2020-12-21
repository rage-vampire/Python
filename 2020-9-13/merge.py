#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : merge.py
# @Author: Lizi
# @Date  : 2020/12/19

list1 = [1,4,5]
list2 = [2,7]

new_list = []

for i in list2:
    list1.append(i)

for j in range(len(list1)):
    if list1[j] > list1[j+1]:
        list1[j], list1[j+1] = list1[j+1], list1[1]
    print(list1)


