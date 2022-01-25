#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : set_demo.py
# @Author: Lizi
# @Date  : 2020/12/16

"""
set():集合是一个无序的不重复的序列。可以使用{ }或者set()创建一个集合。
注意：创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典
创建集合的语法
    1、params={value1,value2,.....}
    2、params =  set(value)
"""

# users = {'1267': {"first": "Larry", "last": "Page"},
#          '2526': {"first": "John", "last": "Freedom"}}
#
# ids = set(users.keys())
# full_name = []
# for user in users.values():
#     full_name.append(f'{user["first"]} {user["last"]}')
#
# print(full_name)
# print(ids)

# 创建一个集合
set1 = {1,2,3,4,'1','2','3','4','aa','bb','aa'}
set2 = set('123456789')
print(set1)
print(set2)
print(set2-set1)     # 集合2中包含而集合1中不包含，即集合2与集合1的差集
print(set1 | set2)   # 集合2或者集合1中包含的所有的元素，即集合1和集合2的并集
print(set1 & set2)   # 集合1和集合2中都包含的元素，即集合1和集合2的交集
print(set1 ^ set2)   # 不同时包含集合1和集合2的元素

# 添加元素
thisset = set(("Google", "Runoob", "Taobao"))
thisset.add(111)
thisset.update([222],['333'])
print(thisset)
