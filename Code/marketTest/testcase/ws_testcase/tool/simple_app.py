# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/5/16
# @Software: PyCharm


from websocket_py3.ws_api.subscribe_server_api import *
from common.common_method import *


class SimpleAppFunc(object):
    def __init__(self, ws_url):
        self.url = ws_url
        self.common = Common()
        self.loop = self.common.getNewLoop()
        self.api = SubscribeApi(self.url, self.loop)

    def connect(self):
        try:
            self.loop.run_until_complete(self.api.client.ws_connect())
        except Exception as e:
            self.common.logger.debug('app connect error:\n{}'.format(e))

    def disconnect(self):
        try:
            self.api.client.disconnect()
        except Exception as e:
            self.common.logger.debug('app disconnect error:\n{}'.format(e))

    def login(self):
        try:
            self.loop.run_until_complete(self.api.LoginReq('app_login', int(time.time() * 1000)))
            asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.loop)
        except Exception as e:
            self.common.logger.debug('app login error:\n{}'.format(e))

    def loginout(self):
        try:
            self.loop.run_until_complete(self.api.LogoutReq(int(time.time() * 1000)))
        except Exception as e:
            self.common.logger.debug('app loginout error:\n{}'.format(e))

    def sub_market(self):
        try:
            sub_type = SubscribeMsgType.SUB_WITH_MARKET
            base_info = [{'exchange': 'HKFE'}]
            start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
            quote_rsp = self.loop.run_until_complete(
                future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                             start_time_stamp=start_time_stamp))
            first_rsp_list = quote_rsp['first_rsp_list']
            assert (self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        except Exception as e:
            self.common.logger.debug('app sub_market error:\n{}'.format(e))

    def unsub_market(self):
        try:
            sub_type = SubscribeMsgType.SUB_WITH_MARKET
            base_info = [{'exchange': 'HKFE'}]
            start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
            quote_rsp = self.loop.run_until_complete(
                future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=None, unbase_info=base_info,
                                             start_time_stamp=start_time_stamp, recv_num=10000))
        except Exception as e:
            self.common.logger.debug('app unsub_market error:\n{}'.format(e))

    def recv_forever(self):
        while True:
            self.loop.run_until_complete(self.api.AppQuoteAllApi(recv_num=100))

    def sub_product(self):
        try:
            sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
            self.product_code = 'HHI'
            base_info = [{'exchange': 'HKFE', 'product_code': self.product_code}]
            start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
            quote_rsp = self.loop.run_until_complete(
                future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                                    start_time_stamp=start_time_stamp))
        except Exception as e:
            self.common.logger.debug('app sub_product error:\n{}'.format(e))

    def unsub_product(self):
        try:
            sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
            # self.product_code = 'HHI'
            base_info = [{'exchange': 'HKFE', 'product_code': self.product_code}]
            start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
            quote_rsp = self.loop.run_until_complete(
                future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=None, unbase_info=base_info,
                                                  start_time_stamp=start_time_stamp, recv_num=10000))
        except Exception as e:
            self.common.logger.debug('app unsub_product error:\n{}'.format(e))

    def sub_instr(self):
        try:
            sub_type = SubscribeMsgType.SUB_WITH_INSTR
            self.code = 'HHI2005'
            base_info = [{'exchange': 'HKFE', 'code': self.code}]
            start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
            quote_rsp = self.loop.run_until_complete(
                future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                                  start_time_stamp=start_time_stamp))
        except Exception as e:
            self.common.logger.debug('app sub_instr error:\n{}'.format(e))

    def unsub_instr(self):
        try:
            sub_type = SubscribeMsgType.SUB_WITH_INSTR
            base_info = [{'exchange': 'HKFE', 'code': self.code}]
            start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
            quote_rsp = self.loop.run_until_complete(
                future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=None, unbase_info=base_info,
                                                    start_time_stamp=start_time_stamp, recv_num=10000))
        except Exception as e:
            self.common.logger.debug('app unsub_instr error:\n{}'.format(e))

    def listen_and_action(self):
        introduce_info = '''
        action == 1 : ws connect
        action == 2 : ws disconnect
        action == 3 : login
        action == 4 : loginout
        action == 5 : sub_market
        action == 6 : unsub_market
        action == a : recv_forever
        action == 7 : sub_product
        action == 8 : unsub_product
        action == 9 : sub_instr
        action == 0 : unsub_instr
        action == a : recv_forever
        action == q : exit
        '''
        self.common.logger.debug('Please input as below shows.{}'.format(introduce_info))
        board = KeyboardListen()
        board.start_listen()
        input_num = 0
        while True:
            if board.input_num > input_num:
                try:
                    input_num = board.input_num
                    # 因可能是右边小键盘数字，所以对应两个key值
                    if board.key in ['1', '97']:
                        self.common.logger.debug('action == 1 : ws connect')
                        self.connect()
                    elif board.key in ['2', '98']:
                        self.common.logger.debug('action == 2 : ws disconnect')
                        self.disconnect()
                    elif board.key in ['3', '99']:
                        self.common.logger.debug('action == 3 : login')
                        self.login()
                    elif board.key in ['4', '100']:
                        self.common.logger.debug('action == 4 : loginout')
                        self.loginout()
                    elif board.key in ['5', '101', '65437']:    # linux's little keyboard is 65437
                        self.common.logger.debug('action == 5 : sub_market')
                        self.sub_market()
                    elif board.key in ['6', '102']:
                        self.common.logger.debug('aaction == 6 : unsub_market')
                        self.unsub_market()
                    elif board.key in ['7', '103']:
                        self.common.logger.debug('action == 7 : sub_product')
                        self.sub_product()
                    elif board.key in ['8', '104']:
                        self.common.logger.debug('action == 8 : unsub_product')
                        self.unsub_product()
                    elif board.key in ['9', '105']:
                        self.common.logger.debug('action == 9 : sub_instr')
                        self.sub_instr()
                    elif board.key in ['0', '96']:
                        self.common.logger.debug('action == 0 : unsub_instr')
                        self.unsub_instr()
                    elif board.key == 'a':
                        self.common.logger.debug('action == a : recv_forever')
                        self.recv_forever()
                    elif board.key == 'q':
                        self.common.logger.debug('action == q : exit')
                        break
                    else:
                        self.common.logger.debug('Input unkonwn! please input as below shows. \n{}'.format(introduce_info))
                except Exception as e:
                    self.common.logger.debug('app listen error:\n', e)


if __name__ == '__main__':
    pass