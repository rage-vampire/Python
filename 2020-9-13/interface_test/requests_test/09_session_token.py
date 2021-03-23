#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 09_session_token.py
# @Author: Lizi
# @Date  : 2020/12/18

import requests

"""
    使用requests库调用华测api的相关接口，完成登录操作，登录后获取token，再去完成获
取用户详情的接口。
"""

login_url = "http://127.0.0.1:5000/api/huace/login"
user_list_url = "http://127.0.0.1:5000/api/huace/userList"

data = {
            "username": "admin",
            "password": "123456"
        }

header = {"Content-Type": "application/json"}
get_session = requests.session()
login_res = get_session.post(login_url, json=data)

# 获取登陆接口的token的值
token = login_res.json()['token']

# 将获取的token 的值更新到原来的header中
new_header = get_session.headers.update({'token': token})

uesr_res = get_session.get(user_list_url)
print(uesr_res.json())
