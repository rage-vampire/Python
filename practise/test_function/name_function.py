# -*- coding:utf-8 -*-
# Filename: name_function.py
# Author: Lizi
# Time: 2019/12/21 17:43
def get_name(first_name,last_name,middle_name=''):
    if middle_name == '':
        full_name = first_name + " " + last_name         # 返回列表类型
    else:
        full_name = first_name + " " + middle_name  + " " + last_name
    return full_name.title()