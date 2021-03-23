#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 06_post_upload_file.py
# @Author: Lizi
# @Date  : 2020/12/15

import requests
import json

URL = "http://www.testingedu.com.cn:8000/index.php/home/Uploadify/imageUp/savepath/head_pic/pictitle/banner/dir/images.html"

file = {
    "file": ("baidu.png",  # 文件名称
             open(r"interface_test/requests_test/baidu.png", 'rb'),  # 文件路径
             'image/png')    # 文件类型
}

data = {"name": "baidu.png"}

# content_type = {'Content-Type': 'multipart/form-data'}
res = requests.post(url=URL, data=data, files=file)

print(res.json())
print(res.status_code)

