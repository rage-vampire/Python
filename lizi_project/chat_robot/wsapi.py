#ws的服务端
# -*- coding: UTF-8 -*-
import time
time.sleep(2)
data='中午'.encode('utf-8')
# 前面加上b声明是二进制数据
s = b'\xe4\xb8\xad\xe5\x8d\x8e\xe4\xba\xba\xe6\xb0\x91\xe5\x85\xb1\xe5\x92\x8c\xe5\x9b\xbd'
# 尝试使用UTF-8解码并输出
print(s.decode('utf-8'))
print(data)
#业务代码，什么业务场景推送
time.sleep(2)
print('message 1')
time.sleep(2)
print('message 3')