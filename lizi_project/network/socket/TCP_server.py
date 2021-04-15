#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : TCP_server.py
# @Author: Lizi
# @Date  : 2020/10/30

import socket
import time

host = socket.gethostname()
port = 8888
bufsize = 1024
size = 5

tcps = socket.socket()
tcps.setsockopt()
tcps.bind((host, port))
tcps.listen(size)

while True:
    print('服务端启动，监听客户端连接')
    conn, addr = tcps.accept()
    print('连接的客户端', addr)
    while True:
        try:
            data = conn.recv(1024)     # 读取已连接客户端发送的消息
        except:
            print('断开的客户端',addr)
            break
        print('客户端发送的内容:', data.decode('utf-8'))
        if not data:
            break

        msg = time.strftime('%Y-%m-%d %X')
        new_msg = '{}{}'.format(msg, data.decode('utf-8'))
        conn.send(new_msg.encode('utf-8'))
    conn.close()
tcps.close()

