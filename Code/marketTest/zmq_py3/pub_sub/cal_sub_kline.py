# -*- coding:utf-8 -*-
# @Filename : cal_sub_tick.py
# @Author : Lizi
# @Time : 2020/6/8 16:40 
# @Software: PyCharm

import zmq
import zmq.asyncio
from google.protobuf import json_format
from py_sqlite.base_sql import *
from pb_files.quote_msg_def_pb2 import *
from pb_files.quote_type_def_pb2 import *


run_flag = True
rec_data = []
common = Common()

sq = SqliteDB()


async def start_sub():    # 创建一个异步函数，即“协程”
    context = zmq.asyncio.Context(io_threads=3)
    sub_socket = context.socket(socket_type=zmq.SUB)
    sub_socket.connect(cal_sub_address)
    sub_socket.setsockopt(zmq.SUBSCRIBE, b'')

    poller = zmq.asyncio.Poller()
    poller.register(sub_socket)

    while run_flag:
        for event in await poller.poll():
            if event[1] & zmq.POLLIN:
                data = event[0].recv().result()
                rec_data = QuoteMsgCarrier()
                rec_data.ParseFromString(data)

# ------------------------------------------ 采集器start------------------------------------------------------


# ------------------------------------------ 计算服务start-------------------------------------------------------
                # 推送分时K线
                if rec_data.type == QuoteMsgType.PUSH_KLINE_MIN:
                    kline_min_data = PushKLineMinData()
                    kline_min_data.ParseFromString(rec_data.data)
                    json_single_data = json_format.MessageToJson(kline_min_data)
                    print("推送分时数据:\n{0}".format(json_single_data))
                    sq.pub_new_record(rec_data.type, kline_min_data, json_single_data)

                # 推送
                elif rec_data.type == QuoteMsgType.PUSH_KLINE:
                    kline_data = PushKLineData()
                    kline_data.ParseFromString(rec_data.data)
                    json_single_data = json_format.MessageToJson(kline_data)
                    print("推送K线数据:\n{0}".format(json_single_data))
                    sq.pub_new_record(rec_data.type, kline_data, json_single_data)


# ------------------------------------------ 计算服务end---------------------------------------------------------

if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(future=start_sub())
