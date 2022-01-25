# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/4/20
# @Software: PyCharm

import asyncio
import websockets
import sys


class BaseWebSocketServer(object):
    def __init__(self):
        pass

    # 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
    async def recv_msg(self, websocket):
        while True:
            recv_text = await websocket.recv()
            response_text = recv_text
            print('response_text:', response_text)
            await websocket.send(response_text)

    async def main_logic(self, websocket, path):
        await self.recv_msg(websocket)

    def run_server(self, ipAddress, port):
        try:
            if sys.platform == 'win32':
                new_loop = asyncio.ProactorEventLoop()
            else:
                new_loop = asyncio.new_event_loop()
            start_server = websockets.serve(self.main_logic, str(ipAddress), int(port), loop=new_loop)
            asyncio.set_event_loop(new_loop)
            asyncio.get_event_loop().run_until_complete(start_server)
            asyncio.get_event_loop().run_forever()
        except Exception as e:
            print('websocket_py3 start server error, please check!\n', e)

if __name__ =='__main__':
    ipAddress = '127.0.0.1'
    port = 10080
    url = ipAddress + ':' + str(port)
    base = BaseWebSocketServer()
    base.run_server(ipAddress, port)
