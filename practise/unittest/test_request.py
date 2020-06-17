# -*- coding:utf-8 -*-
# @Filename : test_request.py 
# @Author : Lizi
# @Time : 2020/4/10 18:35 
# @Software: PyCharm

import requests
param = {'username': 'yanglili', 'pwd':' 123456', 'cpwd': '123456'}
req = requests.post("http://api.nnzhp.cn/api/user/user_reg", params=param)
print(req.text)
print(req.encoding)
