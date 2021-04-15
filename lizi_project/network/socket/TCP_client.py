#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : TCP_client.py
# @Author: Lizi
# @Date  : 2020/10/30

import socket
import time

host = socket.gethostname()
port = 8888
tcp_client = socket.socket()
tcp_client.connect_ex((host, port))
while True:
    data = input('>>').strip()
    if not data:
        break
    tcp_client.send(data.encode('utf-8'))   # 发送消息
    data = tcp_client.recv(1024)     # 读取消息
    if not data:
        break
    print(data.decode('utf-8'))
    tcp_client.close()