#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : websocket_client.py
# @Author: Lizi
# @Date  : 2020/12/25

import json
import time
from websocket import create_connection
import asyncio


class WSclient:
    def __init__(self, addr):
        self.ws = create_connection(addr)  # 创建ws连接

    def send(self, params):
        print("Sending............")
        self.ws.send(json.dumps(params))  # 发送请求数据数据
        print(f'Sending data {params}')

        print('Recving.......')
        result = self.ws.recv()  # 接收服务端的回应数据包数据
        print(f'Received {result}')

    def quit(self):
        self.ws.close()  # 断开连接


t = str(time.time() * 1000).split('.')[0]
params1 = {
    "version": 1,
    "msgNo": t,
    "machNo": "U040119110001",
    "cmd": 1,
    "time": t
}

if __name__ == '__main__':
    address = "ws://127.0.0.1:1234/ws"
    client = WSclient(address)
    client.send(params1)
    # client.quit()
    # print('send end')
