# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/4/29
# @Software: PyCharm

from websocket_py3.ws_api.subscribe_server_api import *
from datetime import datetime


def login():
    start_time_stamp = int(time.time() * 1000)
    asyncio.get_event_loop().run_until_complete(
        future=api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))


# 按市场进行订阅
def market_sub():
    sub_type = SubscribeMsgType.SUB_WITH_MARKET
    base_info = [{'exchange': 'HKFE'}]
    start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
    quote_rsp = asyncio.get_event_loop().run_until_complete(
        future=api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                          start_time_stamp=start_time_stamp))
    first_rsp_list = quote_rsp['first_rsp_list']
    assert (common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
    while True:
        asyncio.get_event_loop().run_until_complete(api.AppQuoteAllApi(recv_num=500))


if __name__ == '__main__':
    common = Common()
    new_loop = common.getNewLoop()
    api = SubscribeApi(union_url, new_loop, is_record=True)
    api.sq.commit('delete from %s;' % (subscribe_table))
    new_loop.run_until_complete(future=api.client.ws_connect())
    login()
    asyncio.run_coroutine_threadsafe(api.hearbeat_job(), new_loop)
    api.logger.debug('Start subscribing：{}'.format(datetime.now()))
    market_sub()
