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
    sub_socket.connect(sub_address)
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
                if rec_data.type == QuoteMsgType.PUSH_TRADE_DATA:
                    trade_data = QuoteTradeData()
                    trade_data.ParseFromString(rec_data.data)
                    json_trade_data = json_format.MessageToJson(trade_data)
                    print("逐笔成交:\n{0}".format(trade_data))
                    json_trade_data = json.loads(json_trade_data)
                    product_code = common.searchDicKV(json_trade_data, 'productCode')
                    instr_code = common.searchDicKV(json_trade_data, 'instrCode')
                    price = int(common.searchDicKV(json_trade_data, 'price'))
                    vol = int(common.searchDicKV(json_trade_data, 'vol'))
                    if 'precision' in json_trade_data.keys():
                        precision = int(common.searchDicKV(json_trade_data, 'precision'))
                    else:
                        precision = 0
                    time = int(common.searchDicKV(json_trade_data, 'time')) / (pow(10, 6))
                    sq.cal_insert_tick(rec_data.type, product_code, instr_code, precision, price, vol, time)

# ------------------------------------------ 采集器end-----------------------------------------------------------


if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(future=start_sub())
