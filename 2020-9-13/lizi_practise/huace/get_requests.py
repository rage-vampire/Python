#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 01_get_requests.py
# @Author: Lizi
# @Date  : 2020/12/15

import requests
import json

"""
requests请求作业：
接口文档：http://49.233.108.117:3000/api

get /topics 主题首页
接收 get 参数
page Number 页数
tab String 主题分类。目前有 ask share job good
limit Number 每一页的主题数量
mdrender String 当为 false 时，不渲染。默认为 true，渲染出现的所有 markdown 格式文本。
示例：/api/v1/topics"""

URL = "http://49.233.108.117:3000/api/v1/topics"

data = {
    "page": 2,
    "tab": "ask",
    "limit": 3,
    "mdrender": "true"
}

res = requests.get(URL, data)
print(res.json())

# 将响应数据以json格式化输出
print(json.dumps(res.json(), indent=4, ensure_ascii=False))


"""
    post /topics 新建主题
    接收 post 参数
    accesstoken String 用户的 accessToken
    title String 标题
    tab String 目前有 ask share job dev。开发新客户端的同学，请务必将你们的测试帖发在 dev 专区，以免污染日常的版面，否则会进行封号一周处理。
    content String 主体内容
"""