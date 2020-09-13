#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_01.py
# @Author: Lizi
# @Date  : 2020/9/9
'''给定一个非空正整数的数组，按照数组内数字重复出现次数，从高到低排序'''

list_a = [1,2,4,1,1,3,6,4,8,7,6]
new_dic = {}
for ele in list_a:
    num = list_a.count(ele)
    if ele not in new_dic:
        new_dic[ele]=num

b = sorted(new_dic.items(), key=lambda item:item[1], reverse=True)
print(b)
# print(new_list)
