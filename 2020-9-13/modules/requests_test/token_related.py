#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : token_related.py
# @Author: Lizi
# @Date  : 2020/12/16

import requests
import json

class Token:
    """
        案例需求：使用requests库调用华测api的相关接口，完成登录操作，登录后获取token，再去完成获
        取用户详情的接口
        服务器路径：E:\02_Person_work\华测学习资料\web自动化\04《自动化基本操作》-木子-2020.11.6\课件资料\04 web自动化切换技巧\webtest\webautotest.py
    """
    def __init__(self):
        self.URL = 'http://127.0.0.1:5000/api/huace'
        self.head = {"Content-Type": "application/json"}

    def login(self):
        # login_url = 'http://127.0.0.1:5000/api/huace/login'
        data = {
            "username": "admin",
            "password": "123456"
        }
        login_res = requests.post(url=self.URL+"/login", json=data, headers=self.head)
        # self.token1 = login_res.json()["token"]
        print(f"获取的token值:{login_res.json()['token']}")
        return login_res


    def user_list(self):
        # userlist_url = "http://127.0.0.1:5000/api/huace/userList"

        self.head["token"] = self.login().json()["token"]
        userlist_res = requests.get(url=self.URL+"/userList", headers=self.head)
        return userlist_res.json()


if __name__ == '__main__':
    token = Token()
    userlist = token.user_list()
    print(userlist)