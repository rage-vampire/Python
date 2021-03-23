#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 08_session_cookie.py
# @Author: Lizi
# @Date  : 2020/12/18

import requests
import json

"""
    使用requests库调用B2C商城登录功能的相关接口，完成登录操作，登录后获取我的订单页面数据。
"""

login_URl = "http://www.testingedu.com.cn:8000/index.php?m=Home&c=User&a=do_login"
order_url = "http://www.testingedu.com.cn:8000/Home/Order/order_list.html"

# 创建session对象
get_session = requests.session()

data = {
    "username": 13800138006,
    "password": 123456,

}
header = {"Content-Type": "application/x-www-form-urlencoded"}
# 发送post请求, 获取登陆的返回数据
login_res = get_session.post(login_URl, data)     # 自动保存cookie信息
# print(login_res.json())
print(json.dumps(login_res.json(), indent=4))

# 发送get请求, 获取订单接口的返回数据
order_res = get_session.get(order_url)
print(order_res.text)

