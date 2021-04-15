#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : socket_client.py
# @Author: Lizi
# @Date  : 2020/10/30

import socket
import sys

s = socket.socket()
host = socket.gethostname()
port = 9999


# 连接服务，指定地址和端口
s.connect((host,port))

# 接收小于1024字节的数据
msg = s.recv(1024)
s.close()
print(msg.decode('utf-8'))