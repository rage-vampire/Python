#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : json_test.py
# @Author: Lizi
# @Date  : 2020/10/29

import json

# json.dumps(): 对数据进行编码
# json.loads(): 对数据进行解码

dic = {'ip': '127.0.0.1',
         'url': 'www.baidu.com',
         'port': 8090}
list_l = ['a', 1, 'b']



json_str = json.dumps(dic)
print('python原始数据：', dic)
print('json对象', json_str)
print(json.dumps(list_l))
print(json.dumps(23))

