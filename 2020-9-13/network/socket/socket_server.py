#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : socket_server.py
# @Author: Lizi
# @Date  : 2020/10/30

import sys
import socket


# 穿件socket对象
server_socket = socket.socket()
# 获取本机主机名
host = socket.gethostname()
port = 9999

# 绑定端口号
server_socket.bind((host, port))

# 设置最大连接数，超过后排队
server_socket.listen(10)

while True:
    # 建立客户端连接
    cilent_socket, addr = server_socket.accept()
    print('连接地址:{}'.format(addr))
    msg = '这是服务端的应答消息'
    cilent_socket.send(msg.encode('utf-8'))
    cilent_socket.close()


