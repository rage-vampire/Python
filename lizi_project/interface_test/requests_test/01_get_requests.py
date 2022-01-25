#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 01_get_requests.py
# @Author: Lizi
# @Date  : 2020/12/14

import requests
import json

URL = 'https://www.baidu.com/'

data = {"id": 1001, 'name': 'yanglili'}     # 传两个参数
# data = {"id": '1001, 1002'}    # 给一个参数赋两个值

# 方法一：get 方法不带参数的请求
# res = requests.get(URL)

# 方法二：get方法带参数
# res = requests.get(URL, data)

# 方法三：或者使用如下方法
res = requests.request('GET', URL, params=data)

# 设置编码格式
res.encoding = 'utf-8'

# 以文本形式显示响应内容
print(res.text)

# 获取响应状态码
print(res.status_code)

# 获取请求的url
print(res.url)

# 查看默认请求编码格式
print(res.encoding)