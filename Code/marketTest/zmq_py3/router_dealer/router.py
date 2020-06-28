# -*- coding: utf-8 -*-
#!/usr/bin/python

import asyncio
import zmq
import zmq.asyncio
from pb_files.common_msg_def_pb2 import *
from pb_files.quote_msg_def_pb2 import *
from pb_files.quote_type_def_pb2 import *

from test_config import *

run_flag=True

async def start():
    context = zmq.asyncio.Context(io_threads=5)
    router_socket = context.socket(socket_type=zmq.ROUTER)
    router_socket.bind(router_address)
    poller = zmq.asyncio.Poller()
    poller.register(router_socket)

    global run_flag
    while run_flag:
        for event in await poller.poll():
            if event[1] & zmq.POLLIN:
                data = event[0].recv().result()
                print("recv:{0}".format(data))

                rev_data = QuoteMsgCarrier()
                rev_data.ParseFromString(data)
                print(rev_data)

                if rev_data.type == QuoteMsgType.SYNC_INSTR_REQ:
                    instr_data = SyncInstrReq()
                    instr_data.ParseFromString(rev_data.data)
                    print(':\n',instr_data)
                await event[0].send(data)
            elif event[1] & zmq.POLLOUT:
                pass
            elif event[2] & zmq.POLLERR:
                print("error:{0},{1}".format(event[0],event[1]))


if __name__=="__main__":
    asyncio.get_event_loop().run_until_complete(future=start())






