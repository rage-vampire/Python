# -*- coding: utf-8 -*-
#!/usr/bin/python

import zmq
import zmq.asyncio
from google.protobuf import json_format
from py_sqlite.base_sql import *
from pb_files.quote_msg_def_pb2 import *
from pb_files.quote_type_def_pb2 import *


run_flag = True
rec_data = []

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

# ------------------------------------------ 采集器start-------------------------------------------------------
                if rec_data.type == QuoteMsgType.PUSH_ORDER_BOOK:
                    order_book = QuoteOrderBookData()
                    order_book.ParseFromString(rec_data.data)
                    json_order_book = json_format.MessageToJson(order_book)
                    print("盘口数据:\n{0}".format(order_book))
                    # file_path = txt_file_save_folder + "order_book.txt"
                    # with open(file_path, 'a') as f:
                    #     f.write("盘口数据:\n" + str(order_book))
                    sq.pub_new_record(rec_data.type, order_book, json_order_book)

                elif rec_data.type == QuoteMsgType.PUSH_TRADE_DATA:
                    trade_data = QuoteTradeData()
                    trade_data.ParseFromString(rec_data.data)
                    json_trade_data = json_format.MessageToJson(trade_data)
                    print("逐笔成交:\n{0}".format(trade_data))
                    file_path = txt_file_save_folder + "Trade_data.txt"
                    # with open(file_path, 'a') as f:
                    #     f.write("逐笔成交:\n" + str(trade_data))
                    sq.pub_new_record(rec_data.type, trade_data, json_trade_data)

                elif rec_data.type == QuoteMsgType.PUSH_BASIC:
                    basic_info = QuoteBasicInfo()
                    basic_info.ParseFromString(rec_data.data)
                    json_basic_info = json_format.MessageToJson(basic_info)
                    print("静态数据:\n{0}".format(basic_info))
                    # file_path = txt_file_save_folder + "Basic_info_sub.txt"
                    # with open(file_path, 'a') as f:
                    #     f.write("静态数据:\n" + str(basic_info))
                    sq.pub_new_record(rec_data.type, basic_info, json_basic_info)

                elif rec_data.type == QuoteMsgType.PUSH_SNAPSHOT:
                    snap_shot = QuoteSnapshot()
                    snap_shot.ParseFromString(rec_data.data)
                    json_snap_shot = json_format.MessageToJson(snap_shot)
                    print("快照数据:\n{0}".format(snap_shot))
                    # file_path= txt_file_save_folder + "snap_shot.txt"
                    # with open(file_path, 'a') as f:
                    #     f.write("快照数据:\n" + str(snap_shot))
                    sq.pub_new_record(rec_data.type, snap_shot, json_snap_shot)

# ------------------------------------------ 采集器end-----------------------------------------------------------

# ------------------------------------------ 计算服务start-------------------------------------------------------
                # 推送分时K线
                elif rec_data.type == QuoteMsgType.PUSH_KLINE_MIN:
                    kline_min_data = PushKLineMinData()
                    kline_min_data.ParseFromString(rec_data.data)
                    json_kline_min_data = json_format.MessageToJson(kline_min_data)
                    print("推送分时数据:\n{0}".format(kline_min_data))
                    # file_path= txt_file_save_folder + "kline_min_data.txt"
                    # with open(file_path, 'a') as f:
                    #     f.write("推送分时数据:\n" + str(kline_min_data))
                    sq.pub_new_record(rec_data.type, kline_min_data, json_kline_min_data)

                # 推送
                elif rec_data.type == QuoteMsgType.PUSH_KLINE:
                    kline_data = PushKLineData()
                    kline_data.ParseFromString(rec_data.data)
                    json_min_data = json_format.MessageToJson(kline_data)
                    print("推送K线数据:\n{0}".format(kline_data))
                    # file_path= txt_file_save_folder + "kline_data.txt"
                    # with open(file_path, 'a') as f:
                    #     f.write("推送K线数据:\n" + str(kline_data))
                    sq.pub_new_record(rec_data.type, kline_data, json_min_data)


# ------------------------------------------ 计算服务end---------------------------------------------------------

if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(future=start_sub())
