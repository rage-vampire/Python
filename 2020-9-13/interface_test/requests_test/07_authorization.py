#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 07_authorization.py
# @Author: Lizi
# @Date  : 2020/12/18

import requests
from base64 import b64encode, b64decode


 # 方法一：
# url = "http://127.0.0.1:5000/api/huace/auth"
# username = "admin"
# password = "huace123456"
# # 通过base64加密后的auth
# new_auth = b64encode(bytes(username, encoding='utf-8')+b":"+bytes(password, encoding="utf-8")).decode("ascii")
# header = {
#     "Authorization": "Basic "+new_auth
# }
# res = requests.post(url=url, headers=header)
# print(res.json())



# 方法二使用session处理auth鉴权
url = "http://127.0.0.1:5000/api/huace/auth"
username = "admin"
password = "huace123456"

get_session = requests.session()
get_session.auth = (username, password)
res = get_session.request("post",url)


print(res.json())
print(get_session.auth)
print(get_session.headers)

