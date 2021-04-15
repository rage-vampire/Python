#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : websocket_server.py
# @Author: Lizi
# @Date  : 2021/4/7


import websockets
import asyncio
import time

class WSserver:

    async def handle(self, websocket, path):

        recv_msg = await websocket.recv()          # 接收客户端的请求数据
        print(f"i received {recv_msg}")
        await websocket.send("server send ok!")      # 发送回应包给客户端

        # while True:
        #     t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        #     if str(t).endswith('0'):
        #         await websocket.send(t)
        #         break

    def run(self):
        ser = websockets.serve(self.handle, "127.0.0.1", 1234)
        asyncio.get_event_loop().run_until_complete(ser)
        asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    ws = WSserver()
    ws.run()


