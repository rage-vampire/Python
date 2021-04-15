#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : dict_sort.py
# @Author: Lizi
# @Date  : 2020/10/13

'''按照字典的key排序'''
def sort_key():

    key_dict = {'a': 1, 'b': 2, 'd': 4, 'c': 3}
    for i in sorted(key_dict):
        new_dict = (i, key_dict[i])
        print(new_dict, end='')

sort_key()
print('')

'''按照value排序'''

def sort_value():
    key_dict = {'a': 1, 'b': 5, 'c': 4, 'd': 3}
    print(sorted(key_dict.items(), key=lambda kv: kv[1]))

sort_value()
