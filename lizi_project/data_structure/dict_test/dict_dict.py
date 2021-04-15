#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : dict_dict.py
# @Author: Lizi
# @Date  : 2020/11/11

user_dict = {
        '2001': {
            'username': 'lizi',
            'passwd': '123456',
            'sex': 'F'},

        '2002': {
            'username': 'huahua',
            'passwd': 'ahfdbg',
            'sex': 'M'}

}
user_list = []
pwd_list = []
# for items in user_dict.items():
#     for i in items[1]:
#         if i == 'username':
#             user_list.append(items[1][i])
#             print(items[1][i])
#         if i == 'passwd':
#             pwd_list.append(items[1][i])
# print(user_list)
# print(pwd_list)

for key in user_dict:
    for j in user_dict[key]:
        if j == 'username':
            user_list.append(user_dict[key][j])
        if j == 'passwd':
            pwd_list.append(user_dict[key][j])
print(user_list)
print(pwd_list)