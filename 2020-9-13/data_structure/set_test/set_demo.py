#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : set_demo.py
# @Author: Lizi
# @Date  : 2020/12/16

users = {'1267': {"first": "Larry", "last": "Page"},
         '2526': {"first": "John", "last": "Freedom"}}

ids = set(users.keys())
full_name = []
for user in users.values():
    full_name.append(f'{user["first"]} {user["last"]}')

print(full_name)
print(ids)