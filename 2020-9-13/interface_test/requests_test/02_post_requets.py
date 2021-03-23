#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 02_post_requets.py
# @Author: Lizi
# @Date  : 2020/12/14

import requests
import json


# URL = 'http://www.testingedu.com.cn:8000/Home/user/login.html'
# h = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
# data = {
#     "username": 13800138006,
#     "password": 123456,
#     "verify_cody": 'M26Q',
# }


URL = 'http://api.test.zhulogic.com/designer_api/account/login_quick'

# 头部参数，Content-Type
head = {'Content-Type': 'application/json'}
data = {
    "phone":15100001111,
    "code": 1234,
    "unionid": "",
    "messageType": 3,
    "channel": "zhulogic"
}

# 方法一：将字典格式的数据转换成json格式传给data
res = requests.post(url=URL, data=json.dumps(data), headers=head)

# 方法二：直接将字典格式的data值传给json参数
# res = requests.post(url=URL, json=data, headers=head)

# 使用requests.request
# res = requests.request('POST', url=URL, json=data, headers=head)


# 设置编码格式
res.encoding = 'utf-8'

# 以文本形式显示响应内容
print(res.text)

# 获取响应状态码
print(res.status_code)

# 获取请求的url
print(res.url)

# 以json字符串形式解析响应内容
print(res.json())
print(type(res))