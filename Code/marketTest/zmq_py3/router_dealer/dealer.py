# -*- coding: utf-8 -*-
#!/usr/bin/python

import zmq
import zmq.asyncio
from google.protobuf import json_format
from py_sqlite.base_sql import *
from pb_files.quote_msg_def_pb2 import *
from pb_files.quote_type_def_pb2 import *
from test_config import *

run_flag = True
sq = SqliteDB()


async def start(send_type):            # 创建一个异步函数，即“协程”
    context = zmq.asyncio.Context(io_threads=5)
    dealer_socket = context.socket(socket_type=zmq.DEALER)
    dealer_socket.connect(dealer_address)
    poller = zmq.asyncio.Poller()
    poller.register(dealer_socket)

    while run_flag:
        for event in await poller.poll():
            print(event[0])
            print(event[1])
            if send_type=='SYNC_INSTR_REQ':
                if event[1] & zmq.POLLOUT:
                    data_send = SyncInstrReq(type=SyncInstrMsgType.ALL_INSTR, date_time=20200408)  # ALL_INSTR 全量同步，INCREMENT_INSTR 增量同步
                    quote_msg = QuoteMsgCarrier(type=QuoteMsgType.SYNC_INSTR_REQ, data=data_send.SerializeToString())
                    # print(quote_msg)
                    quote_msg = quote_msg.SerializeToString()
                    await event[0].send(quote_msg)
                    print("send合约:\n{0}".format(quote_msg))

                if event[1] & zmq.POLLIN:
                    data = event[0].recv().result()
                    print("recv:{0}".format(data))
                    rev_data = QuoteMsgCarrier()
                    rev_data.ParseFromString(data)
                    print(rev_data)

                    if rev_data.type == QuoteMsgType.SYNC_INSTR_RSP:
                        rsp_data = SyncInstrRsp()
                        rsp_data.ParseFromString(rev_data.data)
                        json_rsp_data = json_format.MessageToJson(rsp_data)
                        print('合约信息1111:\n', rsp_data)
                        file_path = txt_file_save_folder + "InstrumentInfos.txt"
                        with open(file_path, 'a') as f:
                            f.write("合约数据:\n" + str(rsp_data))
                        sq.deal_new_record(rev_data.type, rsp_data, json_rsp_data)
                        print(json_rsp_data)
                        pass
            elif send_type == 'SYNC_BASIC_REQ':
                if event[1] & zmq.POLLOUT:
                    data_send = SyncInstrReq(type=SyncInstrMsgType.ALL_INSTR,
                                             date_time=20200408)  # ALL_INSTR 全量同步，INCREMENT_INSTR 增量同步
                    quote_msg = QuoteMsgCarrier(type=QuoteMsgType.SYNC_BASIC_REQ, data=data_send.SerializeToString())
                    # print(quote_msg)
                    quote_msg = quote_msg.SerializeToString()
                    await event[0].send(quote_msg)
                    print("send静态:\n{0}".format(quote_msg))

                if event[1] & zmq.POLLIN:
                    data = event[0].recv().result()
                    print("recv:{0}".format(data))
                    rev_data = QuoteMsgCarrier()
                    rev_data.ParseFromString(data)
                    print(rev_data)


                    if rev_data.type == QuoteMsgType.SYNC_BASIC_RSP:
                        rsp_data = SyncBasicRsp()
                        rsp_data.ParseFromString(rev_data.data)
                        json_rsp_data = json_format.MessageToJson(rsp_data)
                        print("静态数据:\n{0}".format(rsp_data))
                        file_path = txt_file_save_folder + "Basic_info_dealer.txt"
                        with open(file_path, 'a') as f:
                            f.write("静态数据:\n" + str(rsp_data))
                        sq.deal_new_record(rev_data.type, rsp_data, json_rsp_data)
                        print(json_rsp_data)
                        pass

            elif send_type == 'SNAPSHOT_REQ':
                if event[1] & zmq.POLLOUT:
                    data_send = SyncInstrReq(type=SyncInstrMsgType.ALL_INSTR,
                                             date_time=20200408)  # ALL_INSTR 全量同步，INCREMENT_INSTR 增量同步
                    quote_msg = QuoteMsgCarrier(type=QuoteMsgType.SNAPSHOT_REQ, data=data_send.SerializeToString())
                    # print(quote_msg)
                    quote_msg = quote_msg.SerializeToString()
                    await event[0].send(quote_msg)
                    print("send快照:\n{0}".format(quote_msg))

                if event[1] & zmq.POLLIN:
                    data = event[0].recv().result()
                    print("recv:{0}".format(data))
                    rev_data = QuoteMsgCarrier()
                    rev_data.ParseFromString(data)
                    print(rev_data)


                    if rev_data.type == QuoteMsgType.SNAPSHOT_RSP:
                        rsp_data = SnapshotRsp()
                        rsp_data.ParseFromString(rev_data.data)
                        json_rsp_data = json_format.MessageToJson(rsp_data)
                        print("快照数据:\n{0}".format(rsp_data))
                        file_path = txt_file_save_folder + "snap_shot_dealer.txt"
                        with open(file_path, 'a') as f:
                            f.write("快照数据:\n" + str(rsp_data))
                        sq.deal_new_record(rev_data.type, rsp_data, json_rsp_data)
                        print(json_rsp_data)
                        pass

            if event[1] & zmq.POLLERR:
                print("error:{0},{1}".format(event[0], event[1]))
        await asyncio.sleep(delay=5)                                                   # 使用 asyncio.sleep(), 它返回的是一个可等待的对象


if __name__ == "__main__":
    asy = asyncio.get_event_loop()                                                   # 创建一个事件循环
    asy.run_until_complete(future=start('SNAPSHOT_REQ'))                                           # 执行事件队列, 直到最后的一个事件被处理完毕后结束
    #SYNC_INSTR_REQ：合约的    SYNC_BASIC_REQ：静态的   SNAPSHOT_REQ：快照的