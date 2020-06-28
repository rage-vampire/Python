# -*- coding: utf-8 -*-
#!/usr/bin/python

import asyncio
import datetime
import zmq.asyncio
from pb_files.quote_type_def_pb2 import *
from pb_files.quote_msg_def_pb2 import *
from test_config import *

run_flag = True

context = zmq.asyncio.Context(io_threads=1)
pub_socket = context.socket(socket_type=zmq.PUB)
pub_socket.bind(pub_address)
interval = 1

async def Kline_Data():
    send_count = 0
    while run_flag:
        kd_data= KlineData(high=1000, open=500, low=400, close=800,
                       update_date_time=int(datetime.datetime.now().timestamp() * 1000))
        quote_msg = QuoteMsgCarrier(type=QuoteMsgType.PUSH_SNAPSHOT,data=kd_data.SerializeToString())
        print(quote_msg)
        quote_msg = quote_msg.SerializeToString()

        await pub_socket.send(quote_msg)
        print("pub:{0}".format(quote_msg))
        send_count += 1
        if send_count % 1 == 0:
            print("sleeping......{0} seconds".format(interval))
            await asyncio.sleep(interval)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(future=Kline_Data())

