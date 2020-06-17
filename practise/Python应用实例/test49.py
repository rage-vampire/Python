# -*- coding:utf-8 -*-
# @Filename : test49.py 
# @Author : Lizi
# @Time : 2020/4/1 16:23 
# @Software: PyCharm

# 分叉服务器
# from socketserver import TCPServer,ForkingMixIn,StreamRequestHandler
#
#
# class Server(ForkingMixIn,TCPServer):
#     pass
#
#
# class Handler(StreamRequestHandler):
#     def handle(self):
#         addr = self.request.getpeername()
#         print("Got connection from:", addr)
#         self.wfile.write("thank you for connecting")
#
#
# server = Server((' ', 1234), Handler)
# server.serve_forever()


# 线程化服务器

from socketserver import StreamRequestHandler, TCPServer, ThreadingMixIn
import socket


class Server(ThreadingMixIn, TCPServer):
    pass


class Handler(StreamRequestHandler):

    def handle(self):
        client,addr = self.request.getpeername()
        print("Got connection from:", client)
        print("Got connection from:", addr)


host = socket.gethostname()
server = Server(('', 1234), Handler)
server.serve_forever()