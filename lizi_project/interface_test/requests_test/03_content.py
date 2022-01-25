#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 03_content.py
# @Author: Lizi
# @Date  : 2020/12/15

import requests

URL = 'https://www.baidu.com/img/flexible/logo/pc/result.png'

res = requests.get(URL)

print(res.text)
with open('interface_test/requests_test/baidu.png', 'wb') as file:
    file.write(res.content)