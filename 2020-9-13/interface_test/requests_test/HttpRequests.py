#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : HttpRequests.py
# @Author: Lizi
# @Date  : 2020/12/18

import requests


class HttpClientRequest:
    def __init__(self):
        # 创建会话
        self.session = requests.session()
        self.url_pre = 'http://127.0.0.1:5000/api/huace/'
        # 设置初始默认的headers值
        self.session.headers = {'Content-Type': "application/json"}

    def init_headers(self, head):
        """
            当有些接口的'Content-Type'值不是默认方式，可传入head参数，修改headers的值
        """
        if head:
            self.session.headers.update(head)

    def send_request(self, method, api_url, **kwargs):
        """
        method:请求方法
        api_url：接口的参数
        **kwargs：json--->接收json参数
        **kwargs：data--->接收data参数
        **kwargs：params--->接收其他自定义的参数
        """
        self.url = self.url_pre + api_url
        self.json_data = None
        if "json" in kwargs:
            self.json_data = kwargs["json"]

        self.data = None
        if "data" in kwargs:
            self.data = kwargs["data"]

        res = self.session.request(method=method, url=self.url, json=self.json_data, data=self.data)
        self.response = res.json()

        # 提取登陆接口响应中的token的值
        if "params" in kwargs:
            self.val = kwargs["params"]
            self.get_token = self.response[self.val]
            # print("获取的token值：", self.get_token)
            # 将提取的token值更新到headers中
            self.init_headers({self.val: self.get_token})
            # print("更新后的header的值：", self.session.headers)

        return self.response
