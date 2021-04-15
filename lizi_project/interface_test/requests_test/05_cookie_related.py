#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 05_cookie_related.py
# @Author: Lizi
# @Date  : 2020/12/15

import requests
import json

class DainShang:
    def __init__(self):
        self.URL = "http://www.testingedu.com.cn:8000/"
        self.login_URL = "index.php?m=Home&c=User&a=do_login"
        self.order_URL = "Home/Order/order_list.html"

    def login(self):
        """
            登陆，获取登陆后的cookies值
        """
        data = {
            "username": 13800138006,
            "password": 123456,
            "verify_cody": "sf5d"
        }
        content_type = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

        login_res = requests.post(url=f'{self.URL}{self.login_URL}', data=data, headers=content_type)
        # print(json.dumps(login_res.json(), indent=4, ensure_ascii=False))
        # login_res.cookies获取cookies值
        res_cookies = login_res.cookies
        return res_cookies    # 返回cookies值

    def order(self):
        """
            获取订单信息，因为http是无状态的，因此需要传入登陆时的cookies值
        """
        # cookie值，以字典形式保存，将值传给get方法的cookies参数
        cookie = {
            "PHPSESSID": self.login()["PHPSESSID"],
            "is_distribut": self.login()["is_distribut"],
            "is_mobile": self.login()["is_mobile"],
            "uname": self.login()["uname"],
            "user_id": self.login()["user_id"]
        }
        order_res = requests.get(f'{self.URL}{self.order_URL}', cookies=cookie)
        print(order_res.text)
        return order_res.text


if __name__ == '__main__':
    b2c = DainShang()
    order = b2c.order()
    print(order)


