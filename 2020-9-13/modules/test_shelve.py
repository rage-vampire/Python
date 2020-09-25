#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_shelve.py
# @Author: Lizi
# @Date  : 2020/9/24

import shelve
names = ['Bod', 'Alice', 'Jim']
infos = {'name': "Bob", "age": 24, "hobby": "dance" }
days = (23, 34, 26, 25)

with shelve.open('shelve.txt') as f:    # f是一个类似于字典的shelf对象，以key-value方式存储数据，具有字典的所有特点
    f['name'] = names   # 持久化列表
    f['info'] = infos   # 持久化字典
    f['day'] = days     # 持久化元祖

    for k, v in f.items():
        print('{0}:{1}'.format(k, v))


