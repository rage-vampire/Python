# -*- coding:utf-8 -*-
# @Filename : test47.py 
# @Author : Lizi
# @Time : 2020/3/27 14:13 
# @Software: PyCharm

import socket
from socket import SocketKind

# 服务端
s = socket.socket(socket.AF_INET,SocketKind.SOCK_STREAM)
host = socket.gethostname()         # 获取本机IP地址
port = 1234                         # 任意非特权端口
s.bind((host, port))                # 绑定socket到本机地址
s.listen(5)
while True:
    client, addr = s.accept()       # 返回客户端地址
    print('Got connection from:', addr)
    # print()
    client.send("Thank you for connecting！".encode())
    client.close()

# # 客户端
# s = socket.socket()
host = socket.gethostname()
port = 1234
s.connect((host, port))
print(s.recv(1024).decode())
