# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/4/21
# @Software: PyCharm

import unittest

from websocket_py3.ws_api.subscribe_server_api import *
from testcase.zmq_testcase.zmq_record_testcase import CheckZMQ
from common.common_method import *
from common.test_log.ed_log import get_log


class SubscribeTestCases(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.logger = get_log()

    @classmethod
    def setUpClass(cls):
        cls.common = Common()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.new_loop = self.common.getNewLoop()
        asyncio.set_event_loop(self.new_loop)
        self.api = SubscribeApi(union_url, self.new_loop)
        asyncio.get_event_loop().run_until_complete(future=self.api.client.ws_connect())

    def tearDown(self):
        asyncio.set_event_loop(self.new_loop)
        self.api.client.disconnect()

    def inner_zmq_test_case(self, case_name, check_json_list, is_before_data=False, start_sub_time=None):
        suite = unittest.TestSuite()
        suite.addTest(CheckZMQ(case_name))
        suite._tests[0].check_json_list = check_json_list
        suite._tests[0].is_before_data = is_before_data
        suite._tests[0].sub_time = start_sub_time
        runner = unittest.TextTestRunner()
        inner_test_result = runner.run(suite)
        return inner_test_result

    # ------------------------------------------登录-----------------------------------------------------------
    def test_LoginReq01(self):
        '''正常登陆'''
        start_time_stamp = int(time.time() * 1000)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接受时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
    #
    # # ----------------------------------------退出----------------------------------------
    def test_LogoutReq01(self):
        """登陆后退出"""
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.LogoutReq(start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接受时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

    def test_LogoutReq02(self):
        """未登录时，退出登录"""
        start_time_stamp = int(time.time() * 1000)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.LogoutReq(start_time_stamp=start_time_stamp))

        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'retCode')) == 10010)
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'user is not login')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接受时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

    def test_LogoutReq03(self):
        """校验退出之后响应成功，且接不到订阅数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code = 'HHI2009'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.get_event_loop().run_until_complete(future=self.api.SubsQutoMsgReqApi(
            sub_type=sub_type, child_type=None, base_info=base_info, start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.LogoutReq(start_time_stamp=start_time_stamp, recv_num=10))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接受时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

    # ----------------------------------------心跳-----------------------------------------
    def test_HearbeatReqApi01(self):
        """登录成功后50秒内发送心跳"""
        asyncio.get_event_loop().run_until_complete(future=self.api.LoginReq(token='xxxx'))
        time.sleep(3)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.HearbeatReqApi(connid=123))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'connId') == '123')

    def test_HearbeatReqApi02(self):
        """登录成功后，在第一次心跳发送后的50秒内，发送第二次心跳"""
        asyncio.get_event_loop().run_until_complete(future=self.api.LoginReq(token='xxxx'))
        time.sleep(49)
        first_rsp_list1 = asyncio.get_event_loop().run_until_complete(future=self.api.HearbeatReqApi(connid=123))
        self.assertTrue(self.common.searchDicKV(first_rsp_list1[0], 'connId') == '123')
        time.sleep(49)
        first_rsp_list2 = asyncio.get_event_loop().run_until_complete(future=self.api.HearbeatReqApi(connid=123))
        self.assertTrue(self.common.searchDicKV(first_rsp_list2[0], 'connId') == '123')

    # @unittest.skip('耗时较长，先跳过')
    def test_HearbeatReqApi03(self):
        """登录成功后超过50秒发送心跳"""
        asyncio.get_event_loop().run_until_complete(future=self.api.LoginReq(token='xxxx'))
        time.sleep(51)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.HearbeatReqApi(connid=123))
        self.assertTrue(first_rsp_list.__len__() == 0)

    # @unittest.skip('耗时较长，先跳过')
    def test_HearbeatReqApi04(self):
        """登录成功后，在第一次心跳发送后的50秒外，发送第二次心跳"""
        asyncio.get_event_loop().run_until_complete(future=self.api.LoginReq(token='xxxx'))
        time.sleep(49)
        first_rsp_list1 = asyncio.get_event_loop().run_until_complete(future=self.api.HearbeatReqApi(connid=123))
        self.assertTrue(self.common.searchDicKV(first_rsp_list1[0], 'connId') == '123')
        time.sleep(51)
        first_rsp_list2 = asyncio.get_event_loop().run_until_complete(future=self.api.HearbeatReqApi(connid=123))
        self.assertTrue(first_rsp_list2.__len__() == 0)

    # @unittest.skip('不测试')
    def test_HearbeatReqApi05(self):
        """未登录时发送心跳，则无响应"""
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.HearbeatReqApi(connid=123))
        self.assertTrue(first_rsp_list.__len__() == 0)

    # # -------------------------------------------------------测速-------------------------------------------------------
    def test_VelocityReqApi01(self):
        start_time_stamp = int(time.time() * 1000)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.VelocityReqApi(start_time=start_time_stamp))

        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTime')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'sendTime')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvTime')) >
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTime')))

    # --------------------------------------------------订阅start-------------------------------------------------------

    # --------------------------------------------------按合约订阅-------------------------------------------------------
    def test_Instr01(self):
        """按合约代码订阅时，订阅单市场单合约"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code = 'HHI2006'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    # 按合约代码订阅时，订阅单市场多合约
    def test_Instr02(self):
        """按合约代码订阅时，订阅单市场多合约"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code1 = 'HHI2006'
        code2 = 'HHI2009'
        code3 = 'HSI2009'
        code4 = 'HSI2006'
        code5 = 'MCH2009'
        code6 = 'MCH2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2},
                     {'exchange': 'HKFE', 'code': code3}, {'exchange': 'HKFE', 'code': code4},
                     {'exchange': 'HKFE', 'code': code5}, {'exchange': 'HKFE', 'code': code6}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6))

    # 按合约代码订阅时，合约代码为空
    def test_Instr04(self):
        """按合约代码订阅时，合约代码为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code = ''
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'instrument code is null')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    # 按合约代码订阅时，合约代码错误
    def test_Instr05(self):
        """按合约代码订阅时，合约代码错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code = 'xxx'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} ] is unknown".format(code) == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    # 按合约代码订阅时，code传入过期的合约代码
    def test_Instr06(self):
        """按合约代码订阅时，code传入过期的合约代码"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code = 'HHI2001'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} ] is unknown".format(code) == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    # 订阅一个正确的合约代码，一个错误的合约代码
    def test_Instr07(self):
        """订阅一个正确的合约代码，一个错误的合约代码"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code1 = 'MHI2006'
        code2 = 'xxx'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} ] is unknown".format(code2) == self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') is None)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in code1)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in code1)

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验')

        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in code1)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in code1)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in code1)

    # 按合约代码订阅时，exchange错误
    def test_Instr08(self):
        """按合约代码订阅时，合约代码与市场不对应"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        exchange = 'COMEX'
        code = 'MCH2006'
        base_info = [{'exchange': exchange, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} ] is unknown".format(code) == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    def test_Instr09(self):
        """按合约代码订阅时，exchange传入UNKNOWN"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        exchange = 'UNKNOWN'
        code = 'MCH2006'
        base_info = [{'exchange': exchange, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue("exchange is unknown" in self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        # ----------------------------------------------按品种订阅---------------------------------------------------
    def test_Product_001(self):
        """订阅单市场，单品种"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code = 'HHI'
        base_info = [{'exchange': 'HKFE', 'product_code': product_code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, base_info=base_info, start_time_stamp=start_time_stamp))

        first_rsp_list = rsp_list['first_rsp_list']
        before_basic_json_list = rsp_list['before_basic_json_list']
        before_snapshot_json_list = rsp_list['before_snapshot_json_list']
        before_orderbook_json_list = rsp_list['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code)

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code)

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code)

    def test_Product_002(self):
        """
        订阅单市场，多品种
        """
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code1 = 'HHI'
        product_code2 = 'HSI'
        product_code3 = 'MHI'
        product_code4 = 'UCN'
        product_code5 = 'CEU'
        product_code6 = 'LRC'
        product_code7 = 'GDU'
        product_code8 = 'TCH'
        base_info = [{'exchange': 'HKFE', 'product_code': product_code1},
                     {'exchange': 'HKFE', 'product_code': product_code2},
                     {'exchange': 'HKFE', 'product_code': product_code3},
                     {'exchange': 'HKFE', 'product_code': product_code4},
                     {'exchange': 'HKFE', 'product_code': product_code5},
                     {'exchange': 'HKFE', 'product_code': product_code6},
                     {'exchange': 'HKFE', 'product_code': product_code7},
                     {'exchange': 'HKFE', 'product_code': product_code8}]
        asyncio.get_event_loop().run_until_complete(future=self.api.LoginReq(
            token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, base_info=base_info,start_time_stamp=start_time_stamp))

        first_rsp_list = rsp_list['first_rsp_list']
        before_basic_json_list = rsp_list['before_basic_json_list']
        before_snapshot_json_list = rsp_list['before_snapshot_json_list']
        before_orderbook_json_list = rsp_list['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code1, product_code2, product_code3,
                                                                             product_code4, product_code5, product_code6,
                                                                             product_code7, product_code8))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code1, product_code2, product_code3,
                                                                             product_code4, product_code5, product_code6,
                                                                             product_code7, product_code8))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code1, product_code2, product_code3,
                                                                             product_code4, product_code5, product_code6,
                                                                             product_code7, product_code8))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        start_time_stamp = int(time.time() * 1000)
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code1, product_code2, product_code3,
                                                                             product_code4, product_code5, product_code6,
                                                                             product_code7, product_code8))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        start_time_stamp = int(time.time() * 1000)
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code1, product_code2, product_code3,
                                                                             product_code4, product_code5, product_code6,
                                                                             product_code7, product_code8))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        start_time_stamp = int(time.time() * 1000)
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code1, product_code2, product_code3,
                                                                             product_code4, product_code5, product_code6,
                                                                             product_code7, product_code8))

    # 按品种代码订阅时，品种代码为空
    def test_Product_004(self):
        """按品种代码订阅时，品种代码为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code = ''
        base_info = [{'exchange': 'HKFE', 'product_code': product_code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('product code is null' in self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    # 按品种代码订阅时，品种代码错误
    def test_Product_005(self):
        """按品种代码订阅时，品种代码错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code = 'xxx'
        base_info = [{'exchange': 'HKFE', 'product_code': product_code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('product code [ {} ] is unknown'.format(product_code) == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    # 订阅一个正确的品种，一个错误的品种
    def test_Product_006(self):
        """订阅一个正确的品种，一个错误的品种"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code1 = 'HSI'
        product_code2 = 'xxx'
        base_info = [{'exchange': 'HKFE', 'product_code': product_code1},
                     {'exchange': 'HKFE', 'product_code': product_code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("product code [ {} ] is unknown".format(product_code2)
                        in self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in product_code1)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in product_code1)

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code1)

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in product_code1)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in product_code1)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in product_code1)

    def test_Product_007(self):
        """按品种代码订阅时，exchange传入UNKNOWN"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        exchange = 'UNKNOWN'
        product_code = 'MCH'
        base_info = [{'exchange': exchange, 'product_code': product_code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(future=self.api.SubsQutoMsgReqApi(
            sub_type=sub_type, child_type=None, base_info=base_info,start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == "exchange is unknown")
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    # -----------------------------------------按市场订阅-----------------------------------------------------
    # 按市场进行订阅
    def test_Market_001(self):
        """ 按市场订阅，订阅一个市场(code不传入参数)"""
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        base_info = [{'exchange': 'HKFE'}]
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')

        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        quote_rsp = asyncio.get_event_loop().run_until_complete(future=self.api.SubsQutoMsgReqApi(
            sub_type=sub_type, child_type=None, base_info=base_info,start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)


        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

    def test_Market_002(self):
        """ 按市场订阅，订阅一个市场(code传入一个合约代码)"""
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        code = 'MHI2004'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(future=self.api.SubsQutoMsgReqApi(
            sub_type=sub_type, child_type=None, base_info=base_info,start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            if self.common.searchDicKV(info, 'instrCode') == code and i != before_basic_json_list.__len__() - 1:
                continue
            elif self.common.searchDicKV(info, 'instrCode') == code and i == before_basic_json_list.__len__() - 1:
                self.fail()
            else:
                break
        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            if self.common.searchDicKV(info, 'instrCode') == code and i != before_snapshot_json_list.__len__() - 1:
                continue
            elif self.common.searchDicKV(info,
                                         'instrCode') == code and i == before_snapshot_json_list.__len__() - 1:
                self.fail()
            else:
                break

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            if self.common.searchDicKV(info, 'instrCode') == code and i != before_snapshot_json_list.__len__() - 1:
                continue
            elif self.common.searchDicKV(info,
                                         'instrCode') == code and i == before_snapshot_json_list.__len__() - 1:
                self.fail()
            else:
                break

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            if self.common.searchDicKV(info, 'instrCode') == code and i != info_list.__len__() - 1:
                continue
            elif self.common.searchDicKV(info, 'instrCode') == code and i == info_list.__len__() - 1:
                self.fail()
            else:
                break
        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            if self.common.searchDicKV(info, 'instrCode') == code and i != info_list.__len__() - 1:
                continue
            elif self.common.searchDicKV(info, 'instrCode') == code and i == info_list.__len__() - 1:
                self.fail()
            else:
                break
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            if self.common.searchDicKV(info, 'instrCode') == code and i != info_list.__len__() - 1:
                continue
            elif self.common.searchDicKV(info, 'instrCode') == code and i == info_list.__len__() - 1:
                self.fail()
            else:
                break

    def test_Market_003(self):
        """ 按市场订阅，exchange传入UNKNOWN"""
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        base_info = [{'exchange': 'UNKNOWN'}]
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')

        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'exchange is unknown')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.assertTrue(before_basic_json_list.__len__() == 0)
        self.assertTrue(before_snapshot_json_list.__len__() == 0)
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug(u'通过接收接口，筛选出所有数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.AppQuoteAllApi(recv_num=2000))
        self.assertTrue(info_list.__len__() == 0)

    def test_Market_004(self):
        """ 按市场订阅，同时订阅多个市场，其中一个exchange传入UNKNOWN"""
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        base_info = [{'exchange': 'UNKNOWN'}, {'exchange': 'HKFE'}]
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info, recv_num=2,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retMsg') == 'exchange is unknown')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'静态数据校验')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in before_basic_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange'), 'HKFE')

        self.logger.debug(u'前快照数据校验')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in before_snapshot_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange'), 'HKFE')

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in before_orderbook_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange'), 'HKFE')

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange'), 'HKFE')

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange'), 'HKFE')

    # --------------------------------------------订阅快照数据--------------------------------------------------------------

    # 订阅单市场，单合约的快照数据
    def test_QuoteSnapshotApi_01(self):
        """订阅单市场，单合约的快照数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code = 'HHI2006'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code)

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteSnapshotApi_02(self):
        """订阅单市场，多合约的快照数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2009'
        code2 = 'HSI2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=1))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    #  订阅单市场，多合约的快照数据，部分合约代码错误
    def test_QuoteSnapshotApi_03(self):
        """订阅单市场，多合约的快照数据，部分合约代码错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2006'
        code2 = 'XXX'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(future=self.api.SubsQutoMsgReqApi(
            sub_type=sub_type, child_type=child_type, base_info=base_info,start_time_stamp=start_time_stamp, recv_num=2))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue(
            self.common.searchDicKV(first_rsp_list[1], 'retMsg') == "instrument code [ {} ] is unknown".format(code2))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in code1)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteSnapshotApi_04(self):
        """订阅单市场，多合约的快照数据，部分合约代码为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2006'
        code2 = ''
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code is null" in self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in code1)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=200))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code1)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    # 订阅快照数据时，code为空
    def test_QuoteSnapshotApi_05(self):
        """订阅快照数据时，code为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code = ''
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'instrument code is null')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteSnapshotApi_06(self):
        """订阅快照数据时，code错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code = 'xxx'
        code = 'xxxx'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} ] is unknown".format(code) == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteSnapshotApi_07(self):
        """订阅快照数据时，exchange传入UNKNOWN"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code = 'HSI2006'
        exchange = 'UNKNOWN'
        base_info = [{'exchange': exchange, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'exchange is unknown')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    # ------------------------------------------------订阅静态数据---------------------------------------------------
    # 订阅静态
    def test_QuoteBasicInfo_Msg_001(self):
        """ 订阅单个市场、单个合约的静态数据 """
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code = 'HHI2006'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'前快照数据校验')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'前盘口数据校验')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteBasicInfo_Msg_002(self):
        """ 订阅单个市场、多个合约的静态数据 """
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code1 = 'HHI2009'
        code2 = 'HSI2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'静态数据校验')
        self.assertTrue(before_basic_json_list.__len__() == 2)  # 应仅返回两条
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'instrCode') in [code1, code2])
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'instrCode') != self.common.searchDicKV(
            before_basic_json_list[1], 'instrCode'))
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.logger.debug(u'前快照数据校验')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'前盘口数据校验')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))

    def test_QuoteBasicInfo_Msg_003(self):
        """ exchange不为空，code为空"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code = None
        base_info = [{'exchange': 'HKFE', 'code': code}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'instrument code is null')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 不返回数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 不返回数据

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteBasicInfo_Msg_004(self):
        """ exchange传入UNKNOWN"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code = 'MCH2006'
        base_info = [{'exchange': 'UNKNOWN', 'code': code}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'exchange is unknown')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 不返回数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 不返回数据

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteBasicInfo_Msg_005(self):
        """ 传入多个合约code，部分code是错误的code"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code1 = 'xxxx'
        code2 = 'HHI2009'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              recv_num=2, start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} ] is unknown".format(code1) in self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'静态数据校验')
        self.assertTrue(before_basic_json_list.__len__() == 1)  # 仅返回code2的静态数据
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'instrCode') == code2)
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.logger.debug(u'前快照数据校验')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 不返回快照数据

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteBasicInfo_Msg_006(self):
        """ 传入多个合约code，部分code为空"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code1 = ''
        code2 = 'HHI2009'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              recv_num=2, start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code is null" in self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'静态数据校验')
        self.assertTrue(before_basic_json_list.__len__() == 1)  # 仅返回code2的静态数据
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'instrCode') == code2)
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.logger.debug(u'前快照数据校验')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 不返回快照数据

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteBasicInfo_Msg_007(self):
        """ code传入错误的合约信息"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code = 'xxxxx'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} ] is unknown".format(code) == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 不返回数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 不返回数据

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    # -----------------------------------------订阅盘口数据----------------------------------------------------
    def test_QuoteOrderBookDataApi01(self):
        """订阅单市场，单合约的盘口数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code = 'HSI2006'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code)

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteOrderBookDataApi02(self):
        """订阅单市场，多合约盘口数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HSI2006'
        code2 = 'HHI2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteOrderBookDataApi03(self):
        """订阅单市场，多合约的盘口数据，部分合约代码错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HHI2006'
        code2 = 'ddd'
        code3 = 'xxx'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2},
                     {'exchange': 'HKFE', 'code': code3}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} {} ] is unknown".format(code2,code3) == self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') == 'SUB_ORDER_BOOK')
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code1)
        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteOrderBookDataApi04(self):
        """订阅单市场，多合约的盘口数据，部分市场合约代码为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HHI2006'
        code2 = ''
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code is null" == self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') == 'SUB_ORDER_BOOK')
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in code1)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in code1)

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in code1)

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    # 订阅盘口数据时，code为空
    def test_QuoteOrderBookDataApi05(self):
        """订阅盘口数据时，code为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        exchange = 'HKFE'
        code = ''
        base_info = [{'exchange': exchange, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('instrument code is null' == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断是否返回逐笔数据，返回则错误')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteOrderBookDataApi06(self):
        """订阅盘口数据时，exchange传入UNKNOWN"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        exchange = 'UNKNOWN'
        code = 'HHI2009'
        base_info = [{'exchange': exchange, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('exchange is unknown' == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断是否返回逐笔数据，返回则错误')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    # 订阅盘口数据时，code参数错误
    def test_QuoteOrderBookDataApi07(self):
        """订阅盘口数据时，code参数错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        exchange = 'HKFE'
        code = 'xxxx'
        base_info = [{'exchange': exchange, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('instrument code [ {} ] is unknown'.format(code) == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断是否返回逐笔数据，返回则错误')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    # ------------------------------------------------订阅逐笔数据--------------------------------------------------
    # 订阅逐笔数据
    def test_QuoteTradeData_Msg_001(self):
        """ 订阅单个市场、单个合约的逐笔数据"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code = 'HHI2006'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code)

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteTradeData_Msg_002(self):
        """ 订阅单个市场、多个合约的逐笔数据"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'MHI2006'
        code2 = 'HSI2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteTradeData_Msg_003(self):
        """ exchange不为空，code为空"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = None
        code2 = None
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('instrument code is null' == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'判断是否返回逐笔数据，返回则错误')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteTradeData_Msg_004(self):
        """ 订阅多个合约代码，其中一个code错误"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HHI2006'
        code2 = 'xxxx'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} ] is unknown".format(code2) == self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code1)

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteTradeData_Msg_005(self):
        """ exchange传入UNKNOWN"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HHI2009'
        code2 = 'ACC2004'
        base_info = [{'exchange': 'UNKNOWN', 'code': code1}, {'exchange': 'UNKNOWN', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('exchange is unknown' == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteTradeData_Msg_006(self):
        """ code传入错误的合约信息"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code = 'xxxx'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(
            self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'instrument code [ {} ] is unknown'.format(code))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_Subscribe_Msg_01(self):
        """订阅时sub_type传入UNKNOWN_SUB"""
        sub_type = SubscribeMsgType.UNKNOWN_SUB
        code = 'MHI2006'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'subscribeMsgType is unknown')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_Subscribe_Msg_02(self):
        """订阅时sub_type传入UNKNOWN_SUB_CHILD"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.UNKNOWN_SUB_CHILD
        code = 'MHI2006'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'subChildMsgType is unknown')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    # ----------------------------------------------------订阅end-------------------------------------------------------

    # --------------------------------------------------取消订阅start----------------------------------------------------

    # -------------------------------------------------按合约取消订阅-----------------------------------------------------
    def test_UnInstr01(self):
        """订阅一个合约，取消订阅一个合约数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code = 'HSI2006'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'判断取消订阅之后，是否还会收到快照数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到盘口数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到逐笔数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnInstr02(self):
        """订阅多个合约，取消订阅多个合约数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code1 = 'HSI2006'
        code2 = 'MCH2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'判断取消订阅之后，是否还会收到快照数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到盘口数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到逐笔数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnInstr03(self):
        """订阅多个，取消订阅其中的一个合约"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code1 = 'HHI2006'
        code2 = 'HSI2006'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code2)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code2)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code2)

    def test_UnInstr04(self):
        """取消订阅单个合约，合约代码与订阅合约代码不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code1 = 'HSI2006'
        code2 = 'HSI2006'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('SUB_WITH_INSTR: instrument code [ {} ] is no have subscribe'.format(code2) == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

    def test_UnInstr05(self):
        """订阅多个合约，取消订阅多个合约时，其中多个合约代码与订阅的不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code1 = 'HHI2009'
        code2 = 'HSI2006'
        code3 = 'MCH2006'
        code4 = 'xxxx'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}, {'exchange': 'HKFE', 'code': code4}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue(
            self.common.searchDicKV(first_rsp_list[1], 'retMsg') == 'instrument code [ {} ] is unknown'.format(code4))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code2)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code2)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code2)

    def test_UnInstr06(self):
        """按合约取消订阅时，code为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code1 = 'HSI2006'
        code2 = ''
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'instrument code is null')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')

        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

    def test_UnInstr07(self):
        """按合约取消订阅时，exchange为UNKONWN"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code = 'HSI2006'
        exchange1 = 'HKFE'
        exchange2 = 'UNKNOWN'
        base_info1 = [{'exchange': exchange1, 'code': code}]
        base_info2 = [{'exchange': exchange2, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'exchange is unknown')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')

        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    # ----------------------------------------按品种取消订阅----------------------------------------------------
    def test_UnProduct01(self):
        """订阅一个品种，取消订阅一个品种数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code = 'HHI'
        base_info = [{'exchange': 'HKFE', 'product_code': product_code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=None, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp, recv_num=100))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'判断取消订阅之后，是否还会收到快照数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到盘口数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到逐笔数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnProduct02(self):
        """订阅多个品种，取消订阅多个品种数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code1 = 'HHI'
        product_code2 = 'MHI'
        base_info = [{'exchange': 'HKFE', 'product_code': product_code1},
                     {'exchange': 'HKFE', 'product_code': product_code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=None, unbase_info=base_info,
                                                recv_num=100, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'判断取消订阅之后，是否还会收到快照数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到盘口数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到逐笔数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnProduct03(self):
        """订阅多个，取消订阅其中的一个品种"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code1 = 'HHI'
        product_code2 = 'HSI'
        base_info1 = [{'exchange': 'HKFE', 'product_code': product_code1},
                      {'exchange': 'HKFE', 'product_code': product_code2}]
        base_info2 = [{'exchange': 'HKFE', 'product_code': product_code1}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=None, unbase_info=base_info2,
                                                recv_num=100, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code2)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code2)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code2)

    def test_UnProduct04(self):
        """取消订阅单个品种，品种代码与订阅品种代码不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code1 = 'HSI'
        product_code2 = 'HHI'
        product_code3 = 'MHI'
        base_info1 = [{'exchange': 'HKFE', 'product_code': product_code1},
                      {'exchange': 'HKFE', 'product_code': product_code2}]
        base_info2 = [{'exchange': 'HKFE', 'product_code': product_code3}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        start_time_stamp = int(time.time() * 1000)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp,
            recv_num=100))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') ==
                        'SUB_WITH_PRODUCT: product code [ {} ] is no have subscribe'.format(product_code3))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in [product_code1, product_code2])

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in [product_code1, product_code2])

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in [product_code1, product_code2])

    def test_UnProduct05(self):
        """订阅多个品种，取消订阅多个品种时，其中多个品种代码与订阅的不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code1 = 'HHI'
        product_code2 = 'HSI'
        product_code3 = 'MCH'
        product_code4 = 'xxx'
        base_info1 = [{'exchange': 'HKFE', 'product_code': product_code1},
                      {'exchange': 'HKFE', 'product_code': product_code2}]
        base_info2 = [{'exchange': 'HKFE', 'product_code': product_code1},
                      {'exchange': 'HKFE', 'product_code': product_code3},
                      {'exchange': 'HKFE', 'product_code': product_code4}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp,
            recv_num=100))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue('product code [ {} ] is unknown'.format(product_code4) ==
                        self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=800))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code2)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code2)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code2)

    def test_UnProduct06(self):
        """按品种取消订阅时，product_code为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code1 = 'HHI'
        product_code2 = ''
        base_info1 = [{'exchange': 'HKFE', 'product_code': product_code1}]
        base_info2 = [{'exchange': 'HKFE', 'product_code': product_code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp,
            recv_num=50))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'product code is null')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code1)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code1)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code1)

    def test_UnProduct07(self):
        """按品种取消订阅时，exchange为UNKNOWN"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code = 'HHI'
        exchange1 = 'HKFE'
        exchange2 = 'UNKNOWN'
        base_info1 = [{'exchange': exchange1, 'product_code': product_code}]
        base_info2 = [{'exchange': exchange2, 'product_code': product_code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'exchange is unknown')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code)

    def test_UnProduct08(self):
        """通过产品取消订阅后再次取消订阅"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code = 'HHI'
        base_info = [{'exchange': 'HKFE', 'product_code': product_code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info, start_time_stamp=start_time_stamp,
            recv_num=50))

        self.logger.debug(u'再次取消')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info, start_time_stamp=start_time_stamp,
            recv_num=50))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('no have subscribe' == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=1000))
        self.assertTrue(info_list.__len__() == 0)

    # ------------------------------------------------按市场取消订阅--------------------------------------------------------
    # 按市场取消订阅
    def test_UnMarket_001(self):
        """ 按市场取消订阅，取消订阅一个市场，code为空"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        child_type = None
        base_info = [{'exchange': 'HKFE'}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == child_type)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.assertTrue(before_basic_json_list.__len__() > 0)

        # 再取消订阅数据
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp, recv_num=1000))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.logger.debug(u'取消订阅成功，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug(u'取消订阅成功，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug(u'取消订阅成功，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnMarket_002(self):
        """ 按市场取消订阅，取消订阅一个市场，code不为空"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        child_type = None
        code = 'HHI2009'
        base_info = [{'exchange': 'HKFE'}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        self.assertTrue(before_basic_json_list.__len__() > 0)

        # 再取消订阅数据
        base_info = [{'exchange': 'HKFE', 'code': code}]
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp, recv_num=1000))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'取消订阅成功，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug(u'取消订阅成功，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug(u'取消订阅成功，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnMarket_003(self):
        """ 按市场取消订阅，exchange为UNKNOWN"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        child_type = None
        base_info = [{'exchange': 'HKFE'}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == child_type)
        self.assertTrue(before_basic_json_list.__len__() > 0)

        # 再取消订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        base_info = [{'exchange': 'UNKNOWN'}]
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp, recv_num=5000))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'exchange is unknown')
        self.logger.debug(u'取消订阅失败，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        self.logger.debug(u'取消订阅失败，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        self.logger.debug(u'取消订阅失败，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)

    def test_UnMarket_004(self):
        """ 先按合约订阅，再按市场取消订阅"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        child_type = None
        base_info = [{'exchange': 'HKFE', 'code': 'HHI2009'}, {'exchange': 'HKFE', 'code': 'HHI2006'}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == child_type)
        self.assertTrue(before_basic_json_list.__len__() > 0)

        # 再取消订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        cancer_sub_type = SubscribeMsgType.SUB_WITH_MARKET
        cancer_base_info = [{'exchange': 'HKFE'}]
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=cancer_sub_type, unbase_info=cancer_base_info,
                                                start_time_stamp=start_time_stamp, recv_num=1000))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'no have subscribe')
        self.logger.debug(u'取消订阅失败，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        self.logger.debug(u'取消订阅失败，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        self.logger.debug(u'取消订阅失败，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)

    def test_UnMarket_005(self):
        """ 按市场取消后再次取消"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        child_type = None
        base_info = [{'exchange': 'HKFE'}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == child_type)
        self.assertTrue(before_basic_json_list.__len__() > 0)

        # 第一次取消
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp, recv_num=1000))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')

        # 再取消订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp, recv_num=500))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'no have subscribe')
        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    # ------------------------------------------取消订阅快照数据---------------------------------------------------

    def test_UnSnapshot_001(self):
        """取消单个市场，单个合约的快照数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code = 'HHI2006'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')

        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code)
        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp, recv_num=50))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'判断取消订阅之后，是否还会收到快照数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnSnapshot_002(self):
        """取消单个市场,多个合约的快照数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2006'
        code2 = 'MHI2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))
        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')

        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=200))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=20, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'判断取消订阅之后，是否还会收到快照数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnSnapshot_003(self):
        """订阅多个合约快照数据，取消订阅部分快照数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2006'
        code2 = 'MHI2006'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))
        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')

        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=200))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=20, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=200))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code1))

    def test_UnSnapshot_004(self):
        """取消订阅之后，再次发起订阅"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2006'
        code2 = 'MHI2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=20, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

        # 再次发起订阅
        start_time_stamp = int(time.time() * 1000)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=200))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))


    def test_UnSnapshot_005(self):
        """订阅一个合约的快照数据，取消订阅时，合约代码与订阅合约代码不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2006'
        code2 = 'HSI2006'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('SUB_WITH_MSG_DATA: instrument code [ {} ] is no have subscribe'.format(code2) ==
                        self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照口数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=10))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code1))

    def test_UnSnapshot_006(self):
        """订阅一个合约的快照数据，取消订阅时，合约代码错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2006'
        code2 = 'xxx'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} ] is unknown".format(code2) ==
                        self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照口数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=200))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code1))

    def test_UnSnapshot_007(self):
        """订阅多个合约快照数据，取消订阅时部分合约代码与订阅合约代码不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2006'
        code2 = 'MHI2006'
        code3 = 'MCH2012'
        code4 = 'HHI2003'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}, {'exchange': 'HKFE', 'code': code4}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=200))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=20, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} ] is unknown".format(code4) ==
                        self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=10))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code2))

    def test_UnSnapshot_008(self):
        """订阅多个合约快照数据，取消订阅时部分合约代码为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2006'
        code2 = 'MHI2006'
        code3 = None
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=20, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code is null" in self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=10))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code2))

    def test_UnSnapshot_009(self):
        """订阅多个合约快照数据，取消订阅时部分合约代码错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2006'
        code2 = 'MHI2006'
        code3 = 'xxxxx'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=20, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} ] is unknown".format(code3) == self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=10))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code2))

    def test_UnSnapshot_010(self):
        """取消订阅之后，再次发起取消订阅"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2006'
        code2 = 'MHI2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=20, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == "unsubscribe success")
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

        # 再次发起取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=20, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('no have subscribe' == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

    def test_UnSnapshot_011(self):
        """取消订阅快照数据时，exchange传入UNKNOWN"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        exchange = 'HKFE'
        code = 'MHI2006'
        base_info1 = [{'exchange': exchange, 'code': code}]
        base_info2 = [{'exchange': 'UNKNOWN', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp, recv_num=20))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('exchange is unknown' in self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=10))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code))

    def test_UnSnapshot_012(self):
        """取消订阅快照数据时，code为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        exchange = 'HKFE'
        code1 = 'MHI2006'
        code2 = None
        base_info1 = [{'exchange': exchange, 'code': code1}]
        base_info2 = [{'exchange': exchange, 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp, recv_num=20))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code is null" in self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=10))

        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code1))

    # -------------------------------------------------------取消订阅静态数据-------------------------------------------------
    def test_UnQuoteBasicInfo_Msg_001(self):
        """ 取消订阅单个市场、单个合约的静态数据"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code = 'HHI2006'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        # 通过调用行情取消订阅接口，取消订阅数据
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp, recv_num=100))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'取消订阅成功，筛选出静态数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnQuoteBasicInfo_Msg_002(self):
        """ 取消订阅单个市场、多个合约的静态数据"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code1 = 'HHI2006'
        code2 = 'ACC2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        # 通过调用行情取消订阅接口，取消订阅数据
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'取消订阅成功，筛选出静态数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=20))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnQuoteBasicInfo_Msg_003(self):
        """ 先订阅多个合约的静态数据，再取消其中一个合约的静态数据"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code1 = 'HHI2009'
        code2 = 'ACC2006'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        # 通过调用行情取消订阅接口，取消订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'重新订阅成功，筛选出静态数据,并校验')
        # 因静态数据只会在订阅时和开市时才会推送，所以这里不好校验。
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=20))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnQuoteBasicInfo_Msg_004(self):
        """ 先订阅2个合约的静态数据，再取消这2个合约的静态数据，再次订阅"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code1 = 'HHI2009'
        code2 = 'ACC2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        # 通过调用行情取消订阅接口，取消订阅数据
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        # 再次订阅静态数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

    def test_UnQuoteBasicInfo_Msg_005(self):
        """ 取消订阅静态数据，exchange不为空，code为空"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code1 = 'HHI2009'
        code2 = None
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        # 通过调用行情取消订阅接口，取消订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('instrument code is null' in self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

    def test_UnQuoteBasicInfo_Msg_006(self):
        """ exchange传入UNKNOWN"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code = 'HHI2006'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code))

        # 通过调用行情取消订阅接口，取消订阅数据
        base_info = [{'exchange': 'UNKNOWN', 'code': code}]
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('exchange is unknown' in self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'取消订阅失败，筛选出静态数据,并校验')
        # 因静态数据只会在订阅时和开市时才会推送，所以这里不好校验。
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=20))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnQuoteBasicInfo_Msg_007(self):
        """ 静态数据取消，取消后再次取消"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code = 'HHI2009'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code))

        # 通过调用行情取消订阅接口，取消订阅数据
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        # 再次取消
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'no have subscribe')

    def test_UnQuoteBasicInfo_Msg_09(self):
        """ 取消订阅多个合约的静态数据，其中一个code入参错误"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code1 = 'HHI2009'
        code2 = 'ACC2006'
        code3 = 'xxxx'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        # 通过调用行情取消订阅接口，取消订阅数据
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}]
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(sub_type, child_type, base_info, recv_num=50,
                                                start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue('instrument code [ {} ] is unknown'.format(code3) == self.common.searchDicKV(first_rsp_list[1], 'retMsg'))

        self.logger.debug(u'取消订阅成功，筛选出静态数据,并校验')
        # 因静态数据只会在订阅时和开市时才会推送，所以这里不好校验。
        # info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=20))
        # self.assertTrue(info_list.__len__() > 0)

    def test_UnQuoteBasicInfo_Msg_012(self):
        """ code传入错误的合约信息"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code1 = 'HHI2009'
        code2 = 'ACC2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        # 通过调用行情取消订阅接口，取消订阅数据
        # 取消code1，code2入参错误
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        code1 = 'xxx'
        code2 = 'xxx'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('code [ {} {} ] is unknown'.format(code1, code2) in self.common.searchDicKV(first_rsp_list[0], 'retMsg'))

        self.logger.debug(u'取消订阅失败，筛选出静态数据,并校验')
        # 因静态数据只会在订阅时和开市时才会推送，所以这里不好校验。
        # info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=20))
        # self.assertTrue(info_list.__len__() > 0)

    # ------------------------------------------------取消订阅盘口数据-----------------------------------------------
    def test_UnQuoteOrderBookDataApi01(self):
        """取消单个市场，单个合约的盘口数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code = 'HSI2006'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code)

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=500, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'判断取消订阅之后，是否还会收到盘口数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnQuoteOrderBookDataApi02(self):
        """取消单个市场,多个合约的盘口数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HHI2006'
        code2 = 'HSI2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=500, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'判断取消订阅之后，是否还会收到盘口数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnQuoteOrderBookDataApi03(self):
        """订阅多个合约盘口数据，取消订阅部分合约数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HHI2009'
        code2 = 'MHI2006'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=50, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code2))

    def test_UnQuoteOrderBookDataApi04(self):
        """取消订阅之后，再发起订阅"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HSI2006'
        code2 = 'MHI2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=50, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'判断取消订阅之后，是否还会收到盘口数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        # 再次发起订阅
        start_time_stamp = int(time.time() * 1000)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

    def test_UnQuoteOrderBookDataApi05(self):
        """订阅一个合约的盘口数据，取消订阅时，合约代码与订阅合约代码不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HHI2006'
        code2 = 'HSI2006'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code1)

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=50, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue("SUB_WITH_MSG_DATA: instrument code [ {} ] is no have subscribe".format(code2) ==
                        self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code1))

    def test_UnQuoteOrderBookDataApi06(self):
        """订阅一个合约的盘口数据，取消订阅时，合约代码错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HHI2006'
        code2 = 'xxx'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code1)

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp, recv_num=50))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} ] is unknown".format(code2) == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=200))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code1))

    def test_UnQuoteOrderBookDataApi07(self):
        """订阅多个合约盘口数据，取消订阅时部分合约代码与订阅合约代码不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HHI2009'
        code2 = 'MHI2006'
        code3 = 'MCH2012'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=50, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("SUB_WITH_MSG_DATA: instrument code [ {} ] is no have subscribe".format(code3) ==
                        self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code2))

    def test_UnQuoteOrderBookDataApi08(self):
        """订阅多个合约盘口数据，取消订阅时部分合约代码错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HHI2009'
        code2 = 'MHI2006'
        code3 = 'xxx'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=200))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=100, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} ] is unknown".format(code3) == self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=200))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code2))

    def test_UnQuoteOrderBookDataApi09(self):
        """订阅多个合约盘口数据，取消订阅时部分合约代码为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HHI2009'
        code2 = 'MHI2006'
        code3 = None
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=50, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue('instrument code is null' in self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code2))

    def test_UnQuoteOrderBookDataApi_10(self):
        """取消订阅盘口数据后再次取消"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        exchange = 'HKFE'
        code = 'MCH2006'
        base_info = [{'exchange': exchange, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code)

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == "unsubscribe success")
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        # 再次取消
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('no have subscribe' == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

    def test_UnQuoteOrderBookDataApi_11(self):
        """取消订阅盘口数据时，exchange传入UNKNOWN"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        exchange1 = 'HKFE'
        exchange2 = 'UNKNOWN'
        code = 'HHI2006'
        base_info1 = [{'exchange': exchange1, 'code': code}]
        base_info2 = [{'exchange': exchange2, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code)

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=500, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('exchange is unknown' == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code))

    def test_UnQuoteOrderBookDataApi_012(self):
        """取消订阅盘口数据时，code为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        exchange = 'HKFE'
        code1 = 'MCH2006'
        code2 = ''
        base_info1 = [{'exchange': exchange, 'code': code1}]
        base_info2 = [{'exchange': exchange, 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code1)

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('instrument code is null' == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code1))

    # ------------------------------------------------取消订阅逐笔数据-----------------------------------------------------
    def test_UnQuoteTradeData_Msg_001(self):
        """ 取消订阅单个市场、单个合约的逐笔数据"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code = 'HSI2006'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        # self.assertTrue(info_list.__len__() == 1)  # 应仅返回一条
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code)

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=20, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == "unsubscribe success")
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'取消订阅逐笔数据后，校验逐笔数据接收情况')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnQuoteTradeData_Msg_002(self):
        """ 取消订阅单个市场、多个合约的逐笔数据"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HHI2006'
        code2 = 'HSI2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=20))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug('订阅逐笔成功后至少返回一笔逐笔')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() >= 1)  # 应最少返回一条
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == "unsubscribe success")
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'取消订阅逐笔数据后，校验逐笔数据接收情况')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnQuoteTradeData_Msg_003(self):
        """ 先订阅多个合约的逐笔数据，再取消其中一个合约的逐笔数据"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HHI2006'
        code2 = 'HSI2006'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug('订阅逐笔成功后至少返回一笔逐笔')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() >= 1)  # 应最少返回一条
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        # 取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=100, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == "unsubscribe success")
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'取消订阅逐笔数据后，校验逐笔数据接收情况')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() > 0)
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue((self.common.searchDicKV(info_list[0], 'instrCode') == code2))
        self.assertTrue((self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE'))

    def test_UnQuoteTradeData_Msg_004(self):
        """ 先订阅一个合约的逐笔数据，再取消这个合约的逐笔数据，再次订阅逐笔数据"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HSI2006'
        code2 = 'MHI2006'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug('订阅逐笔成功后至少返回一笔逐笔')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() >= 1)  # 应最少返回一条
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        #  取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=20, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == "unsubscribe success")
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'取消订阅逐笔数据后，校验逐笔数据接收情况')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() == 0)

        # 再次订阅
        self.logger.debug('再次订阅逐笔数据')
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug('订阅逐笔成功后至少返回一笔逐笔')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=10000))
        self.assertTrue(info_list.__len__() >= 1)  # 应最少返回一条
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

    def test_UnQuoteTradeData_Msg_005(self):
        """先订阅一个合约的逐笔，取消订阅时合约代码与订阅时的合约代码不一致"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HSI2006'
        code2 = 'MHI2006'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug('订阅逐笔成功后至少返回一笔逐笔')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=1000))
        self.assertTrue(info_list.__len__() >= 1)  # 应最少返回一条
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code1)

        #  取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=20, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue("SUB_WITH_MSG_DATA: instrument code [ {} ] is no have subscribe".format(code2) ==
                        self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code1)

    def test_UnQuoteTradeData_Msg_006(self):
        """先订阅一个合约的逐笔，取消订阅时合约代码为空"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HSI2006'
        code2 = None
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug('订阅逐笔成功后至少返回一笔逐笔')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() >= 1)  # 应最少返回一条
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code1)

        #  取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=20, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code is null" == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=300))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code1)

    def test_UnQuoteTradeData_Msg_007(self):
        """先订阅一个合约的逐笔，取消订阅时合约代码错误"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HSI2006'
        code2 = 'xxx'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug('订阅逐笔成功后至少返回一笔逐笔')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() >= 1)  # 应最少返回一条
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code1)

        #  取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=20, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(
            "instrument code [ {} ] is unknown".format(code2) == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code1)

    def test_UnQuoteTradeData_Msg_008(self):
        """先订阅多个合约的逐笔，取消订阅时部分合约代码与订阅时的合约代码不一致"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HSI2006'
        code2 = 'MHI2006'
        code3 = 'MHI2009'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug('订阅逐笔成功后至少返回一笔逐笔')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() >= 1)  # 应最少返回一条
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        #  取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=20, start_time_stamp=start_time_stamp))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("SUB_WITH_MSG_DATA: instrument code [ {} ] is no have subscribe".format(code3) ==
                        self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code2)

    def test_UnQuoteTradeData_Msg_009(self):
        """先订阅多个合约的逐笔，取消订阅时部分合约代码为空"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HSI2006'
        code2 = 'MHI2006'
        code3 = None
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug('订阅逐笔成功后至少返回一笔逐笔')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() >= 1)  # 应最少返回一条
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        #  取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=20, start_time_stamp=start_time_stamp))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code is null" == self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code2)

    def test_UnQuoteTradeData_Msg_010(self):
        """先订阅多个合约的逐笔，取消订阅时部分合约代码错误"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HSI2006'
        code2 = 'MHI2006'
        code3 = 'xxx'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug('订阅逐笔成功后至少返回一笔逐笔')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() >= 1)  # 应最少返回一条
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') in (code1, code2))

        #  取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=500, start_time_stamp=start_time_stamp))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} ] is unknown".format(code3) == self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code2)

    def test_UnQuoteTradeData_Msg_011(self):
        """ exchange传入UNKNOWN"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code = 'HSI2006'
        base_info1 = [{'exchange': 'HKFE', 'code': code}]
        base_info2 = [{'exchange': 'UNKNOWN', 'code': code}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug('订阅逐笔成功后至少返回一笔逐笔')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() >= 1)  # 应最少返回一条
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code)

        # 取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue("exchange is unknown" == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'取消订阅逐笔数据失败后，校验逐笔数据接收情况')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() >= 1)  # 应最少返回一条
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code)

    def test_UnQuoteTradeData_Msg_012(self):
        """ 取消之后，再次取消"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code = 'HSI2006'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug('订阅逐笔成功后至少返回一笔逐笔')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() >= 1)  # 应最少返回一条
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.searchDicKV(info_list[0], 'exchange') == 'HKFE')
        self.assertTrue(self.common.searchDicKV(info_list[0], 'instrCode') == code)

        # 取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue('unsubscribe success' == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'取消订阅逐笔数据后，校验逐笔数据接收情况')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() == 0)

        # 再次取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue("no have subscribe" in self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

    def test_UnSubsQutoMsgApi01(self):
        """取消订阅时，sub_type传入UNKNOWN_SUB"""
        start_time_stamp = int(time.time() * 1000)
        sub_type1 = SubscribeMsgType.SUB_WITH_INSTR
        sub_type2 = 'UNKNOWN_SUB'
        exchange = 'HKFE'
        code = 'MCH2006'
        base_info = [{'exchange': exchange, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type1, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type2, unchild_type=None, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('unSubscribeMsgType is unknown' == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code))

    def test_UnSubsQutoMsgApi02(self):
        """取消订阅时，sub_type与订阅时的sub_type不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type1 = SubscribeMsgType.SUB_WITH_INSTR
        sub_type2 = SubscribeMsgType.SUB_WITH_PRODUCT
        exchange = 'HKFE'
        code = 'MCH2006'
        product_code = 'MCH'
        base_info1 = [{'exchange': exchange, 'code': code}]
        base_info2 = [{'exchange': exchange, 'product_code': product_code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type1, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type2, unchild_type=None, unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('no have subscribe'.format(product_code) == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code))

    def test_UnSubsQutoMsgApi03(self):
        """取消订阅时，child_type为UNKNOWN_SUB_CHILD"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type1 = SubChildMsgType.SUB_ORDER_BOOK
        child_type2 = 'UNKNOWN_SUB_CHILD'
        exchange = 'HKFE'
        code = 'MCH2009'
        base_info = [{'exchange': exchange, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type1, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type2, unbase_info=base_info,
                                                recv_num=50, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('unSubChildMsgType is unknown' == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=10))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code))

    def test_UnSubsQutoMsgApi04(self):
        """取消订阅时，child_type与订阅时的child_type不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type1 = SubChildMsgType.SUB_ORDER_BOOK
        child_type2 = SubChildMsgType.SUB_TRADE_DATA
        exchange = 'HKFE'
        code = 'MCH2009'
        base_info = [{'exchange': exchange, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type1, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type2, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue('this child type no have subscribe' == self.common.searchDicKV(first_rsp_list[0], 'retMsg'))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=10))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue((self.common.searchDicKV(info, 'instrCode') == code))

    # -------------------------------------------取消订阅end---------------------------------------------------

    # ------------------------------------------------外盘期货-----------------------------------------------------------

    # ------------------------------------------------按合约订阅---------------------------------------------------------
    def test_Instr_01(self):
        """按合约代码订阅时，订阅单市场单合约"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        exchange1 = 'NYMEX'
        code1 = 'QMmain'
        # code2 = 'QMmain'
        # code3 = 'NGmain'
        # code4 = 'BZmain'
        # exchange3 = 'COMEX'
        # code5 = 'GCmain'
        # exchange4 = 'CBOT'
        # code6 = 'YMmonth'
        # exchange5 = 'CME'
        # code7 = 'MESmain'
        # exchange6 = 'SGX'
        # code8 = 'CNmain'
        base_info = [{'exchange': exchange1, 'code': code1}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1))

    def test_Instr_02(self):
        """按合约代码订阅时，订阅多市场多合约"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        exchange2 = 'NYMEX'
        code1 = 'CLmain'
        code2 = 'QMmain'
        code3 = 'NGmain'
        code4 = 'BZmain'
        exchange3 = 'COMEX'
        code5 = 'GCmain'
        exchange4 = 'CBOT'
        code6 = 'YMmonth'
        exchange5 = 'CME'
        code7 = 'MESmain'
        exchange6 = 'SGX'
        code8 = 'CNmain'
        base_info = [{'exchange': exchange2, 'code': code1}, {'exchange': exchange2, 'code': code2},
                     {'exchange': exchange2, 'code': code3}, {'exchange': exchange2, 'code': code4},
                     {'exchange': exchange3, 'code': code5}, {'exchange': exchange4, 'code': code6},
                     {'exchange': exchange5, 'code': code7}, {'exchange': exchange6, 'code': code8}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)

        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7, code8))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7, code8))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7, code8))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验')
        start_time_stamp = int(time.time() * 1000)
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7, code8))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        start_time_stamp = int(time.time() * 1000)
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7, code8))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        start_time_stamp = int(time.time() * 1000)
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7, code8))

    def test_Instr_03(self):
        """按合约代码订阅时，同时订阅香港和外期"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        exchange1 = 'HKFE'
        code1 = 'HHI2006'
        code2 = 'MHI2006'
        code3 = 'HSI2006'
        code4 = 'MCH2006'
        exchange2 = 'NYMEX'
        code5 = 'CLmain'
        code6 = 'QMmain'
        code7 = 'NGmain'
        code8 = 'BZmain'
        exchange3 = 'COMEX'
        code9 = 'GCmain'
        exchange4 = 'CBOT'
        code10 = 'YMmonth'
        exchange5 = 'CME'
        code11 = 'MESmain'
        exchange6 = 'SGX'
        code12 = 'CNmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange2, 'code': code5}, {'exchange': exchange2, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange3, 'code': code9}, {'exchange': exchange4, 'code': code10},
                     {'exchange': exchange5, 'code': code11}, {'exchange': exchange6, 'code': code12}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
            exchange1, exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
            code1, code2, code3, code4, code5, code6, code7, code8, code9, code10, code11, code12))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
                code1, code2, code3, code4, code5, code6, code7, code8, code9, code10, code11, code12))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
                code1, code2, code3, code4, code5, code6, code7, code8, code9, code10, code11, code12))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
                code1, code2, code3, code4, code5, code6, code7, code8, code9, code10, code11, code12))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
                code1, code2, code3, code4, code5, code6, code7, code8, code9, code10, code11, code12))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
                code1, code2, code3, code4, code5, code6, code7, code8, code9, code10, code11, code12))

        # ----------------------------------------------按品种订阅-----------------------------------------------------------
    def test_Product_01(self):
        """
        按品种订阅订阅外期，单市场
        """
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        exchange = 'SGX'
        # exchange = 'COMEX'
        # exchange = 'NYMEX'
        # exchange = 'CME'
        # exchange = 'SGX'
        product_code = 'TW'
        # product_code = 'GC'
        # product_code = 'CL'
        # product_code = 'MES'
        # product_code = 'CN'
        base_info = [{'exchange': exchange, 'product_code': product_code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code))

    def test_Product_02(self):
        """
        按品种订阅订阅外期，多市场
        """
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        exchange1 = 'NYMEX'
        exchange2 = 'COMEX'
        exchange3 = 'CBOT'
        exchange4 = 'CME'
        exchange5 = 'SGX'
        product_code1 = 'CL'
        product_code2 = 'GC'
        product_code3 = 'ZS'
        product_code4 = 'MES'
        product_code5 = 'CN'
        base_info = [{'exchange': exchange1, 'product_code': product_code1},
                     {'exchange': exchange2, 'product_code': product_code2},
                     {'exchange': exchange3, 'product_code': product_code3},
                     {'exchange': exchange4, 'product_code': product_code4},
                     {'exchange': exchange5, 'product_code': product_code5}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, base_info=base_info,start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
                product_code1, product_code2, product_code3, product_code4, product_code5))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
                product_code1, product_code2, product_code3, product_code4, product_code5))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
                product_code1, product_code2, product_code3, product_code4, product_code5))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
                product_code1, product_code2, product_code3, product_code4, product_code5))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
                product_code1, product_code2, product_code3, product_code4, product_code5))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
                product_code1, product_code2, product_code3, product_code4, product_code5))

    def test_Product_03(self):
        """
        按品种订阅，同时订阅香港和外期
        """
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        exchange1 = 'NYMEX'
        exchange2 = 'COMEX'
        exchange3 = 'CBOT'
        exchange4 = 'CME'
        exchange5 = 'SGX'
        exchange6 = 'HKFE'
        product_code1 = 'CL'
        product_code2 = 'GC'
        product_code3 = 'YM'
        product_code4 = 'MES'
        product_code5 = 'CN'
        product_code6 = 'HHI'
        base_info = [{'exchange': exchange1, 'product_code': product_code1},
                     {'exchange': exchange2, 'product_code': product_code2},
                     {'exchange': exchange3, 'product_code': product_code3},
                     {'exchange': exchange4, 'product_code': product_code4},
                     {'exchange': exchange5, 'product_code': product_code5},
                     {'exchange': exchange6, 'product_code': product_code6}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
                product_code1, product_code2, product_code3, product_code4, product_code5, product_code6))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
                product_code1, product_code2, product_code3, product_code4, product_code5, product_code6))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
                product_code1, product_code2, product_code3, product_code4, product_code5, product_code6))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
                product_code1, product_code2, product_code3, product_code4, product_code5, product_code6))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
                product_code1, product_code2, product_code3, product_code4, product_code5, product_code6))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (
                exchange1, exchange2, exchange3, exchange4, exchange5, exchange6))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
                product_code1, product_code2, product_code3, product_code4, product_code5, product_code6))
    # ----------------------------------------------按市场订阅---------------------------------------------------

    # 按市场进行订阅
    def test_Market_001_01(self):
        """ 按市场订阅，订阅一个市场(code不传入参数)"""
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        base_info = [
             # {'exchange': 'NYMEX'},
             {'exchange': 'CBOT'},
             # {'exchange': 'CME'},
             # {'exchange': 'COMEX'},
             # {'exchange': 'SGX'}
                     ]
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')

        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        quote_rsp = asyncio.get_event_loop().run_until_complete(future=self.api.SubsQutoMsgReqApi(
            sub_type=sub_type, child_type=None, base_info=base_info, start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.QuoteOrderBookDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

    def test_Market_001_02(self):
        """ 按市场订阅，订阅一个外期一个港期市场(code不传入参数)"""
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        base_info = [{'exchange': 'NYMEX'},
                     {'exchange': 'HKFE'}
                     ]
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')

        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        quote_rsp = asyncio.get_event_loop().run_until_complete(future=self.api.SubsQutoMsgReqApi(
            sub_type=sub_type, child_type=None, base_info=base_info, start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.QuoteOrderBookDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

    def test_Market_002_01(self):
        """ 按市场订阅，订阅一个市场(code传入一个合约代码)"""
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        code = '6C2012'
        exchange='CBOT'
        base_info = [{'exchange': exchange, 'code': code}]
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(future=self.api.SubsQutoMsgReqApi(
            sub_type=sub_type, child_type=None, base_info=base_info, start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            if self.common.searchDicKV(info, 'instrCode') == code and i != before_basic_json_list.__len__() - 1:
                continue
            elif self.common.searchDicKV(info, 'instrCode') == code and i == before_basic_json_list.__len__() - 1:
                self.fail()
            else:
                break
        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            if self.common.searchDicKV(info, 'instrCode') == code and i != before_snapshot_json_list.__len__() - 1:
                continue
            elif self.common.searchDicKV(info,
                                         'instrCode') == code and i == before_snapshot_json_list.__len__() - 1:
                self.fail()
            else:
                break

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            if self.common.searchDicKV(info, 'instrCode') == code and i != before_snapshot_json_list.__len__() - 1:
                continue
            elif self.common.searchDicKV(info,
                                         'instrCode') == code and i == before_snapshot_json_list.__len__() - 1:
                self.fail()
            else:
                break

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            if self.common.searchDicKV(info, 'instrCode') == code and i != info_list.__len__() - 1:
                continue
            elif self.common.searchDicKV(info, 'instrCode') == code and i == info_list.__len__() - 1:
                self.fail()
            else:
                break
        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.QuoteOrderBookDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            if self.common.searchDicKV(info, 'instrCode') == code and i != info_list.__len__() - 1:
                continue
            elif self.common.searchDicKV(info, 'instrCode') == code and i == info_list.__len__() - 1:
                self.fail()
            else:
                break
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            if self.common.searchDicKV(info, 'instrCode') == code and i != info_list.__len__() - 1:
                continue
            elif self.common.searchDicKV(info, 'instrCode') == code and i == info_list.__len__() - 1:
                self.fail()
            else:
                break

    # --------------------------------------------订阅外盘快照数据--------------------------------------------------------
    def test_QuoteSnapshotApi_001(self):
        """订阅单市场，单合约的快照数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        exchange1 = 'CBOT'
        code1 = 'ZTmain'
        base_info = [{'exchange': exchange1, 'code': code1}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange1)
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1))

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteSnapshotApi_002(self):
        """订阅多市场，多合约的快照数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        exchange1 = 'CME'
        code1 = '6A2006'
        code2 = '6B2006'
        code3 = '6Cmain'
        code4 = '6Nmain'
        code5 = '6Emain'
        code6 = '6Jmain'
        exchange2 = 'NYMEX'
        code7 = 'CLmain'
        code8 = 'QMmain'
        code9 = 'NGmain'
        code10 = 'BZmain'
        exchange3 = 'SGX'
        code11 = 'NKmain'
        code12 = 'TWmain'
        code13 = 'CNmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                           code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10, code11, code12,
                                                                           code13))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10, code11, code12,
                                                                           code13))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10, code11, code12,
                                                                           code13))

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteSnapshotApi_003(self):
        """同时订阅外期和港期的快照数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        exchange1 = 'CME'
        code1 = '6A2006'
        code2 = '6B2006'
        code3 = '6Cmain'
        code4 = '6Nmain'
        code5 = '6Emain'
        code6 = '6Jmain'
        exchange2 = 'HKFE'
        code7 = 'HHI2006'
        code8 = 'MHI2006'
        code9 = 'HSI2006'
        code10 = 'MCH2006'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10))

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteSnapshotApi_004(self):
        """订阅多市场，多合约的快照数据，部分合约代码错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        exchange1 = 'CBOT'
        code1 = 'YM2006'
        code2 = 'YMmain'
        code3 = 'ZTmain'
        code4 = 'ZFmain'
        code5 = 'ZNmain'
        code6 = 'xxxx'
        exchange2 = 'COMEX'
        code7 = 'GCmain'
        code8 = 'SImain'
        code9 = 'HGmain'
        code10 = 'QOmain'
        code11 = 'QCmain'
        code12 = 'QImain'
        code13 = 'xxxx'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange2, 'code': code11}, {'exchange': exchange2, 'code': code12},
                     {'exchange': exchange2, 'code': code13}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(future=self.api.SubsQutoMsgReqApi(
            sub_type=sub_type, child_type=child_type, base_info=base_info, start_time_stamp=start_time_stamp,
            recv_num=2))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue(
            self.common.searchDicKV(first_rsp_list[1], 'retMsg') == "instrument code [ {} {} ] is unknown".format(code6,code13))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code7,
                                                                           code8, code9, code10, code11, code12,code13))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code7,
                                                                           code8, code9, code10, code11, code12))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code7,
                                                                           code8, code9, code10, code11, code12))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code7,
                                                                           code8, code9, code10, code11, code12))

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    # --------------------------------------------------订阅外盘期货静态数据---------------------------------------------

    def test_QuoteBasicInfo_Msg_01(self):
        """ 订阅多市场、多合约的静态数据 """
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        exchange1 = 'CME'
        code1 = '6A2006'
        code2 = '6B2006'
        code3 = '6Cmain'
        code4 = '6Nmain'
        code5 = '6Emain'
        code6 = '6Jmain'
        exchange2 = 'NYMEX'
        code7 = 'CL2006'
        code8 = 'QMmain'
        code9 = 'NGmain'
        code10 = 'BZmain'
        exchange3 = 'SGX'
        code11 = 'NKmain'
        code12 = 'TWmain'
        code13 = 'CNmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10, code11, code12,
                                                                           code13))

        self.logger.debug(u'前快照数据校验')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteBasicInfo_Msg_02(self):
        """ 同时订阅外期和港期的静态数据 """
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        exchange1 = 'CME'
        code1 = '6A2006'
        code2 = '6B2006'
        code3 = '6Cmain'
        code4 = '6Nmain'
        code5 = '6Emain'
        code6 = '6Jmain'
        exchange2 = 'HKFE'
        code7 = 'HHI2006'
        code8 = 'MHI2006'
        code9 = 'MCH2006'
        code10 = 'HSI2006'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10))

        self.logger.debug(u'前快照数据校验')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteBasicInfo_Msg_03(self):
        """ 多市场，多合约，部分合约代码错误"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        exchange1 = 'CBOT'
        code1 = 'YM2006'
        code2 = 'YMmain'
        code3 = 'ZTmonth'
        code4 = 'ZFmain'
        code5 = 'ZNmain'
        code6 = 'xxxx'
        exchange2 = 'COMEX'
        code7 = 'GCmain'
        code8 = 'SImain'
        code9 = 'HGmain'
        code10 = 'QOmain'
        code11 = 'QCmain'
        code12 = 'QImain'
        code13 = 'xxxx'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange2, 'code': code11}, {'exchange': exchange2, 'code': code12},
                     {'exchange': exchange2, 'code': code13}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              recv_num=2, start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retMsg') == "instrument code [ {} {} ] is unknown".format(code6,code13))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'静态数据校验')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code7,
                                                                           code8, code9, code10, code11, code12))

        self.logger.debug(u'前快照数据校验')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 不返回快照数据

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    # ---------------------------------------------订阅外盘期货盘口数据--------------------------------------------------

    def test_QuoteOrderBookDataApi_01(self):
        """订阅多市场，多合约的盘口数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        exchange1 = 'CME'
        code1 = '6A2006'
        code2 = '6B2006'
        code3 = '6Cmain'
        code4 = '6Nmain'
        code5 = '6Emain'
        code6 = '6Jmain'
        exchange2 = 'NYMEX'
        code7 = 'CL2007'
        code8 = 'QMmain'
        code9 = 'NGmain'
        code10 = 'BZmain'
        exchange3 = 'SGX'
        code11 = 'NKmain'
        code12 = 'TWmain'
        code13 = 'CNmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10, code11, code12,
                                                                           code13))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10, code11, code12,
                                                                           code13))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10, code11, code12,
                                                                           code13))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10, code11, code12,
                                                                           code13))

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteOrderBookDataApi_02(self):
        """同时订阅外期和港期的盘口数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        exchange1 = 'CME'
        code1 = '6A2006'
        code2 = '6B2006'
        code3 = '6Cmain'
        code4 = '6Nmain'
        code5 = '6Emain'
        code6 = '6Jmain'
        exchange2 = 'HKFE'
        code7 = 'HHI2006'
        code8 = 'MHI2006'
        code9 = 'MCH2006'
        code10 = 'HSI2006'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10))

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteOrderBookDataApi_03(self):
        """订阅多市场，多合约的盘口数据，部分合约代码错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        exchange1 = 'CBOT'
        code1 = 'YM2006'
        code2 = 'YMmain'
        code3 = 'ZTmonth'
        code4 = 'ZFmain'
        code5 = 'ZNmain'
        code6 = 'xxxx'
        exchange2 = 'COMEX'
        code7 = 'GCmain'
        code8 = 'SImain'
        code9 = 'HGmain'
        code10 = 'QOmain'
        code11 = 'QCmain'
        code12 = 'QImain'
        code13 = 'xxxx'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange2, 'code': code11}, {'exchange': exchange2, 'code': code12},
                     {'exchange': exchange2, 'code': code13}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        before_orderbook_json_list = quote_rsp['before_orderbook_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue("instrument code [ {} {} ] is unknown".format(code6, code13) == self.common.searchDicKV(first_rsp_list[1],'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') == 'SUB_ORDER_BOOK')
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code7,
                                                                           code8, code9, code10, code11, code12))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code7,
                                                                           code8, code9, code10, code11, code12))

        self.logger.debug(u'校验前盘口数据')
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_orderbook_json_list.__len__()):
            info = before_orderbook_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code7,
                                                                           code8, code9, code10, code11, code12))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code7,
                                                                           code8, code9, code10, code11, code12))

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug("判断是否返回逐笔数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    # -----------------------------------------订阅外盘期货逐笔数据-----------------------------------------------------
    def test_QuoteTradeData_Msg_01(self):
        """ 订阅多个市场、多个合约的逐笔数据"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        exchange1 = 'CME'
        code1 = '6A2006'
        code2 = '6B2006'
        code3 = '6Cmain'
        code4 = '6Nmain'
        code5 = '6Emain'
        code6 = '6Jmain'
        exchange2 = 'NYMEX'
        code7 = 'CL2007'
        code8 = 'QMmain'
        code9 = 'NGmain'
        code10 = 'BZmain'
        exchange3 = 'SGX'
        code11 = 'NKmain'
        code12 = 'TWmain'
        code13 = 'CNmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10, code11, code12,
                                                                           code13))

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteTradeData_Msg_02(self):
        """ 同时订阅外期和港期的逐笔数据"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        exchange1 = 'CME'
        code1 = '6A2006'
        code2 = '6B2006'
        code3 = '6Cmain'
        code4 = '6Nmain'
        code5 = '6Emain'
        code6 = '6Jmain'
        exchange2 = 'HKFE'
        code7 = 'HHI2006'
        code8 = 'MHI2006'
        code9 = 'MCH20065'
        code10 = 'HSI2006'
        exchange3 = 'SGX'
        code11 = 'NKmain'
        code12 = 'TWmain'
        code13 = 'CNmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6,
                                                                           code7, code8, code9, code10, code11, code12,
                                                                           code13))

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QuoteTradeData_Msg_03(self):
        """ 订阅多个市场，多合约，部分合约代码错误"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        exchange1 = 'CBOT'
        code1 = 'YM2006'
        code2 = 'YMmain'
        code3 = 'ZTmonth'
        code4 = 'ZFmain'
        code5 = 'ZNmain'
        code6 = 'xxxx'
        exchange2 = 'COMEX'
        code7 = 'GCmain'
        code8 = 'SImain'
        code9 = 'HGmain'
        code10 = 'QOmain'
        code11 = 'QCmain'
        code12 = 'QImain'
        code13 = 'xxxx'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange2, 'code': code11}, {'exchange': exchange2, 'code': code12},
                     {'exchange': exchange2, 'code': code13}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue(
            "instrument code [ {} {} ] is unknown".format(code6, code13) == self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code7,
                                                                           code8, code9, code10, code11, code12))

        self.logger.debug("判断是否返回静态数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回盘口数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug("判断是否返回快照数据，如果返回则错误")
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    # -----------------------------------------------取消订阅外盘------------------------------------------------------
    # ------------------------------------------外盘，按合约取消订阅--------------------------------------------------

    def test_UnInstr_01(self):
        """订阅单个市场一个合约，取消订阅一个合约数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        exchange = 'CME'
        code = 'ES2009'
        base_info = [{'exchange': exchange, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'判断取消订阅之后，是否还会收到快照数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到盘口数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到逐笔数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnInstr_02(self):
        """订阅多个市场多个合约，取消订阅多个市场的合约数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        exchange1 = 'CME'
        code1 = 'ESmain'
        code2 = 'NQmain'
        code3 = 'NIYmain'
        exchange2 = 'NYMEX'
        code4 = 'QM2009'
        code5 = 'NG2009'
        code6 = 'BZ2008'
        exchange3 = 'CBOT'
        code7 = 'ZWmain'
        exchange4 = 'COMEX'
        code8 = 'HGmonth'
        exchange5 = 'SGX'
        code9 = 'CN2007'
        base_info = [{'exchange': exchange1, 'code': code1},{'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3},{'exchange': exchange2, 'code': code4},
                     {'exchange': exchange2, 'code': code5},{'exchange': exchange2, 'code': code6},
                     {'exchange': exchange3, 'code': code7},{'exchange': exchange4, 'code': code8},
                     {'exchange': exchange5, 'code': code9}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2,exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2,code3, code4,code5, code6,code7, code8,code9))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
            code1, code2, code3, code4, code5, code6, code7, code8, code9))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
            code1, code2, code3, code4, code5, code6, code7, code8, code9))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
            code1, code2, code3, code4, code5, code6, code7, code8, code9))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
            code1, code2, code3, code4, code5, code6, code7, code8, code9))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'判断取消订阅之后，是否还会收到快照数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到盘口数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到逐笔数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnInstr_03(self):
        """订阅多个市场多个合约，取消订阅某部分合约数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        exchange1 = 'CME'
        code1 = 'ES2007'
        code2 = 'NQ2009'
        code3 = 'NIY2008'
        exchange2 = 'NYMEX'
        code4 = 'QM2009'
        code5 = 'NG2009'
        code6 = 'NIY2008'
        exchange3 = 'NYMEX'
        code7 = 'ZWmain'
        exchange4 = 'COMEX'
        code8 = 'HGmonth'
        exchange5 = 'SGX'
        code9 = 'CN2007'
        base_info = [{'exchange': exchange1, 'code': code1},{'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3},{'exchange': exchange2, 'code': code4},
                     {'exchange': exchange2, 'code': code5},{'exchange': exchange2, 'code': code6},
                     {'exchange': exchange3, 'code': code7},{'exchange': exchange4, 'code': code8},
                     {'exchange': exchange5, 'code': code9}]
        base_info2 = [{'exchange': exchange1, 'code': code3}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2,exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2,code3, code4,code5, code6,code7, code8,code9))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
            code1, code2, code3, code4, code5, code6, code7, code8, code9))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
            code1, code2, code3, code4, code5, code6, code7, code8, code9))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
            code1, code2, code3, code4, code5, code6, code7, code8, code9))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
            code1, code2, code3, code4, code5, code6, code7, code8, code9))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
                code1, code2, code4, code5, code6, code7, code8, code9))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
                code1, code2, code4, code5, code6, code7, code8, code9))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=1000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (
                code1, code2, code4, code5, code6, code7, code8, code9))

    # -----------------------------------------------外盘，按品种取消订阅-------------------------------------------------

    def test_UnProduct_01(self):
        """订阅一个市场一个品种，取消订阅一个品种数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        exchange = 'CBOT'
        product_code = 'ZF'
        base_info = [{'exchange': exchange, 'product_code': product_code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=None, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'判断取消订阅之后，是否还会收到快照数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到盘口数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到逐笔数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnProduct_02(self):
        """订阅多个市场多个品种，取消订阅多个品种数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        exchange1 = 'CME'
        product_code1 = 'MNQ'
        exchange2 = 'NYMEX'
        product_code2 = 'BZ'
        exchange3 = 'CBOT'
        product_code3 = 'NYM'
        exchange4 = 'COMEX'
        product_code4 = 'GC'
        exchange5 = 'SGX'
        product_code5 = 'NK'
        base_info = [{'exchange': exchange1, 'product_code': product_code1},
                     {'exchange': exchange2, 'product_code': product_code2},
                     {'exchange': exchange3, 'product_code': product_code3},
                     {'exchange': exchange4, 'product_code': product_code4},
                     {'exchange': exchange5, 'product_code': product_code5}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1,exchange2,exchange3,exchange4,exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code1,product_code2,product_code3,product_code4,product_code5))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
            product_code1, product_code2, product_code3, product_code4, product_code5))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
            product_code1, product_code2, product_code3, product_code4, product_code5))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
            product_code1, product_code2, product_code3, product_code4, product_code5))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
            product_code1, product_code2, product_code3, product_code4, product_code5))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=None, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'判断取消订阅之后，是否还会收到快照数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到盘口数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'判断取消订阅之后，是否还会收到逐笔数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnProduct_03(self):
        """订阅多个市场多个品种，取消订阅部分品种数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        exchange1 = 'CME'
        product_code1 = 'MNQ'
        exchange2 = 'NYMEX'
        product_code2 = 'BZ'
        exchange3 = 'CBOT'
        product_code3 = 'MYM'
        exchange4 = 'COMEX'
        product_code4 = 'GC'
        exchange5 = 'SGX'
        product_code5 = 'NK'
        base_info = [{'exchange': exchange1, 'product_code': product_code1},
                     {'exchange': exchange2, 'product_code': product_code2},
                     {'exchange': exchange3, 'product_code': product_code3},
                     {'exchange': exchange4, 'product_code': product_code4},
                     {'exchange': exchange5, 'product_code': product_code5}]
        base_info2 = [{'exchange': exchange5, 'product_code': product_code5}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1,exchange2,exchange3,exchange4,exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code1,product_code2,product_code3,product_code4,product_code5))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
            product_code1, product_code2, product_code3, product_code4, product_code5))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
            product_code1, product_code2, product_code3, product_code4, product_code5))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
            product_code1, product_code2, product_code3, product_code4, product_code5))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
            product_code1, product_code2, product_code3, product_code4, product_code5))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=None, unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
                product_code1, product_code2, product_code3, product_code4))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
                product_code1, product_code2, product_code3, product_code4))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(
                self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3, exchange4, exchange5))
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (
                product_code1, product_code2, product_code3, product_code4))

    # ----------------------------------------------外盘，按市场取消订阅--------------------------------------------------

    def test_UnMarket_01(self):
        """ 按市场取消订阅，取消订阅一个市场"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        child_type = None
        exchange = 'COMEX'
        base_info = [{'exchange': exchange}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        # 再取消订阅数据
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp, recv_num=1000))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'取消订阅成功，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug(u'取消订阅成功，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug(u'取消订阅成功，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnMarket_02(self):
        """ 按市场取消订阅，取消订阅多个市场"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        child_type = None
        exchange1 = 'CBOT'
        exchange2 = 'NYMEX'
        exchange3 = 'HKFE'
        base_info = [{'exchange': exchange1}, {'exchange': exchange2}, {'exchange': exchange3}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        # 再取消订阅数据
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp, recv_num=1000))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'取消订阅成功，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug(u'取消订阅成功，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug(u'取消订阅成功，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() == 0)

    # -------------------------------------------取消订阅外盘期货快照数据----------------------------------------------------

    def test_UnSnapshot_01(self):
        """订阅多个市场，取消多个市场，多个合约的快照数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        exchange1 = 'CME'
        code1 = '6S2006'
        code2 = 'E72006'
        code3 = 'J7main'
        code4 = 'NQmain'
        code5 = 'MNQmain'
        code6 = 'ESmain'
        exchange2 = 'NYMEX'
        code7 = 'CLmain'
        code8 = 'QM2007'
        code9 = 'NG2007'
        code10 = 'BZ2007'
        exchange3 = 'CBOT'
        code11 = 'ZBmain'
        code12 = 'ZCmain'
        code13 = 'ZSmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=5000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                       code8, code9, code10, code11, code12, code13))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp, recv_num=50))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'判断取消订阅之后，是否还会收到快照数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnSnapshot_02(self):
        """订阅多个市场，取消一个市场，多个合约的快照数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        exchange1 = 'CME'
        code1 = '6A2006'
        code2 = '6B2006'
        code3 = '6Cmain'
        code4 = '6Nmain'
        code5 = '6Emain'
        code6 = '6Jmain'
        exchange2 = 'NYMEX'
        code7 = 'CL2006'
        code8 = 'QMmain'
        code9 = 'NGmain'
        code10 = 'BZmain'
        exchange3 = 'CBOT'
        code11 = 'ZSmain'
        code12 = 'ZMmain'
        code13 = 'ZWmain'
        base_info1 = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        base_info2 = [{'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                      {'exchange': exchange3, 'code': code13}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=8000))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                           code8, code9, code10, code11, code12, code13))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp, recv_num=50))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                           code8, code9, code10))

    def test_UnSnapshot_03(self):
        """取消订阅之后，再次发起订阅"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        exchange1 = 'CME'
        code1 = '6A2006'
        code2 = '6B2006'
        code3 = '6Cmain'
        code4 = '6Nmain'
        code5 = '6Emain'
        code6 = '6Jmain'
        exchange2 = 'NYMEX'
        code7 = 'CL2006'
        code8 = 'QMmain'
        code9 = 'NGmain'
        code10 = 'BZmain'
        exchange3 = 'SGX'
        code11 = 'NKmain'
        code12 = 'TWmain'
        code13 = 'CNmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                           code8, code9, code10, code11, code12, code13))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp, recv_num=50))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'判断取消订阅之后，是否还会收到快照数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)


        #  再次订阅
        start_time_stamp = int(time.time() * 1000)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                           code8, code9, code10, code11, code12, code13))


    def test_UnSnapshot_04(self):
        """订阅多个市场，取消订阅时，部分合约代码与订阅时的代码不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        exchange1 = 'CME'
        code1 = '6A2006'
        code2 = '6B2006'
        code3 = '6Cmain'
        code4 = '6Nmain'
        code5 = '6Emain'
        code6 = '6Jmain'
        exchange2 = 'NYMEX'
        code7 = 'CL2006'
        code8 = 'QMmain'
        code9 = 'NGmain'
        code10 = 'BZmain'
        exchange3 = 'CBOT'
        code11 = 'ZSmain'
        code12 = 'ZMmain'
        code13 = 'ZWmain'
        code14 = 'xxxx'
        base_info1 = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        base_info2 = [{'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                      {'exchange': exchange3, 'code': code13}, {'exchange': exchange3, 'code': code14}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_SNAPSHOT')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                           code8, code9, code10, code11, code12, code13))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp, recv_num=50))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retMsg') == 'instrument code [ {} ] is unknown'.format(code14))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                           code8, code9, code10))

    # -----------------------------------------------取消订阅外盘期货静态数据---------------------------------------------

    def test_UnQuoteBasicInfo_Msg_01(self):
        """ 订阅多个市场，取消订阅多个市场，多个合约的静态数据"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        exchange1 = 'CME'
        code1 = '6S2006'
        code2 = 'E72006'
        code3 = 'J7main'
        code4 = 'NQmain'
        code5 = 'MNQmain'
        code6 = 'ESmain'
        exchange2 = 'NYMEX'
        code7 = 'CLmain'
        code8 = 'QM2007'
        code9 = 'NG2007'
        code10 = 'BZ2007'
        exchange3 = 'CBOT'
        code11 = 'ZBmain'
        code12 = 'ZCmain'
        code13 = 'ZSmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                           code8, code9, code10, code11, code12, code13))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp, recv_num=100))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'取消订阅成功，筛选出静态数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnQuoteBasicInfo_Msg_02(self):
        """ 订阅多个市场，取消订阅一个市场，多个合约的静态数据"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        exchange1 = 'CME'
        code1 = '6S2006'
        code2 = 'E72006'
        code3 = 'J7main'
        code4 = 'NQmain'
        code5 = 'MNQmain'
        code6 = 'ESmain'
        exchange2 = 'NYMEX'
        code7 = 'CLmain'
        code8 = 'QM2007'
        code9 = 'NG2007'
        code10 = 'BZ2007'
        exchange3 = 'CBOT'
        code11 = 'ZBmain'
        code12 = 'ZCmain'
        code13 = 'ZSmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        base_info2 = [{'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                           code8, code9, code10, code11, code12, code13))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp, recv_num=100))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'取消订阅成功，筛选出静态数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnQuoteBasicInfo_Msg_03(self):
        """ 取消订阅，再次发起订阅"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        exchange1 = 'CME'
        code1 = '6S2006'
        code2 = 'E72006'
        code3 = 'J7main'
        code4 = 'NQmain'
        code5 = 'MNQmain'
        code6 = 'ESmain'
        exchange2 = 'NYMEX'
        code7 = 'CLmain'
        code8 = 'QM2007'
        code9 = 'NG2007'
        code10 = 'BZ2007'
        exchange3 = 'SGX'
        code11 = 'NKmain'
        code12 = 'TWmain'
        code13 = 'CNmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                           code8, code9, code10, code11, code12, code13))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp, recv_num=100))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'取消订阅成功，筛选出静态数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        # 再次订阅
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

    def test_UnQuoteBasicInfo_Msg_04(self):
        """ 订阅多个市场，取消订阅一个市场，部分合约代码与订阅时的代码不一致"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        exchange1 = 'CME'
        code1 = '6S2006'
        code2 = 'E72006'
        code3 = 'J7main'
        code4 = 'NQmain'
        code5 = 'MNQmain'
        code6 = 'ESmain'
        exchange2 = 'NYMEX'
        code7 = 'CLmain'
        code8 = 'QM2007'
        code9 = 'NG2007'
        code10 = 'BZ2007'
        exchange3 = 'CBOT'
        code11 = 'ZBmain'
        code12 = 'ZCmain'
        code13 = 'ZSmain'
        code14 = 'xxxx'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        base_info2 = [{'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}, {'exchange': exchange3, 'code': code14}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                           code8, code9, code10, code11, code12, code13))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp, recv_num=100))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == 'unsubscribe success')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retMsg') == 'instrument code [ {} ] is unknown'.format(code14))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'取消订阅成功，筛选出静态数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    # ------------------------------------------取消订阅外盘期货盘口数据------------------------------------------------

    def test_UnQuoteOrderBookDataApi_01(self):
        """订阅多个市场，取消订阅多个市场的盘口数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        exchange1 = 'CME'
        code1 = '6S2006'
        code2 = 'E72006'
        code3 = 'J7main'
        code4 = 'NQmain'
        code5 = 'MNQmain'
        code6 = 'ESmain'
        exchange2 = 'NYMEX'
        code7 = 'CLmain'
        code8 = 'QM2007'
        code9 = 'NG2007'
        code10 = 'BZ2007'
        exchange3 = 'CBOT'
        code11 = 'ZBmain'
        code12 = 'ZCmain'
        code13 = 'ZSmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=8000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                           code8, code9, code10, code11, code12, code13))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=500, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'判断取消订阅之后，是否还会收到盘口数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnQuoteOrderBookDataApi_02(self):
        """订阅多个市场，取消订阅一个市场的盘口数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        exchange1 = 'CME'
        code1 = '6S2006'
        code2 = 'E72006'
        code3 = 'J7main'
        code4 = 'NQmain'
        code5 = 'MNQmain'
        code6 = 'ESmain'
        exchange2 = 'NYMEX'
        code7 = 'CLmain'
        code8 = 'QM2007'
        code9 = 'NG2007'
        code10 = 'BZ2007'
        exchange3 = 'CBOT'
        code11 = 'ZBmain'
        code12 = 'ZCmain'
        code13 = 'ZSmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        base_info2 = [{'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                       code8, code9, code10, code11, code12, code13))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=500, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10))

    def test_UnQuoteOrderBookDataApi_03(self):
        """取消订阅后，再次订阅"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        exchange1 = 'CME'
        code1 = '6S2006'
        code2 = 'E72006'
        code3 = 'J7main'
        code4 = 'NQmain'
        code5 = 'MNQmain'
        code6 = 'ESmain'
        exchange2 = 'NYMEX'
        code7 = 'CLmain'
        code8 = 'QM2007'
        code9 = 'NG2007'
        code10 = 'BZ2007'
        exchange3 = 'SGX'
        code11 = 'NKmain'
        code12 = 'TWmain'
        code13 = 'CNmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                       code8, code9, code10, code11, code12, code13))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=500, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'判断取消订阅之后，是否还会收到盘口数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)

    #     再次订阅
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                           code8, code9, code10, code11, code12, code13))


    def test_UnQuoteOrderBookDataApi_04(self):
        """订阅多个市场，取消订阅一个市场，部分合约代码与订阅时的合约代码不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        exchange1 = 'CME'
        code1 = '6S2006'
        code2 = 'E72006'
        code3 = 'J7main'
        code4 = 'NQmain'
        code5 = 'MNQmain'
        code6 = 'ESmain'
        exchange2 = 'NYMEX'
        code7 = 'CLmain'
        code8 = 'QM2007'
        code9 = 'NG2007'
        code10 = 'BZ2007'
        exchange3 = 'CBOT'
        code11 = 'ZBmain'
        code12 = 'ZCmain'
        code13 = 'ZSmain'
        code14 = 'xxxx'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        base_info2 = [{'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                      {'exchange': exchange3, 'code': code13}, {'exchange': exchange3, 'code': code14}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_basic_json_list.__len__()):
            info = before_basic_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'校验前快照数据')
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(before_snapshot_json_list.__len__()):
            info = before_snapshot_json_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                       code8, code9, code10, code11, code12, code13))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=500, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retMsg') == 'instrument code [ {} ] is unknown'.format(code14))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10))

    # ------------------------------------------取消订阅外盘期货逐笔数据------------------------------------------------

    def test_UnQuoteTradeData_Msg_01(self):
        """ 订阅多个市场，取消订阅多个市场的逐笔数据"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        exchange1 = 'CME'
        code1 = '6S2006'
        code2 = 'E72006'
        code3 = 'J7main'
        code4 = 'NQmain'
        code5 = 'MNQmain'
        code6 = 'ESmain'
        exchange2 = 'NYMEX'
        code7 = 'CLmain'
        code8 = 'QM2007'
        code9 = 'NG2007'
        code10 = 'BZ2007'
        exchange3 = 'CBOT'
        code11 = 'ZBmain'
        code12 = 'ZCmain'
        code13 = 'ZSmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                           code8, code9, code10, code11, code12, code13))
        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=20, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == "unsubscribe success")
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'取消订阅逐笔数据后，校验逐笔数据接收情况')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnQuoteTradeData_Msg_02(self):
        """ 订阅多个市场，取消订阅一个市场的逐笔数据"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        exchange1 = 'CME'
        code1 = '6S2006'
        code2 = 'E72006'
        code3 = 'J7main'
        code4 = 'NQmain'
        code5 = 'MNQmain'
        code6 = 'ESmain'
        exchange2 = 'NYMEX'
        code7 = 'CLmain'
        code8 = 'QM2007'
        code9 = 'NG2007'
        code10 = 'BZ2007'
        exchange3 = 'CBOT'
        code11 = 'ZBmain'
        code12 = 'ZCmain'
        code13 = 'ZSmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        base_info2 = [{'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                           code8, code9, code10, code11, code12, code13))
        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=20, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == "unsubscribe success")
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                                           code8, code9, code10))

    def test_UnQuoteTradeData_Msg_03(self):
        """ 取消订阅之后再次订阅"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        exchange1 = 'CME'
        code1 = '6S2006'
        code2 = 'E72006'
        code3 = 'J7main'
        code4 = 'NQmain'
        code5 = 'MNQmain'
        code6 = 'ESmain'
        exchange2 = 'NYMEX'
        code7 = 'CLmain'
        code8 = 'QM2007'
        code9 = 'NG2007'
        code10 = 'BZ2007'
        exchange3 = 'SGX'
        code11 = 'NKmain'
        code12 = 'TWmain'
        code13 = 'CNmain'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                           code8, code9, code10, code11, code12, code13))
        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=20, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == "unsubscribe success")
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'取消订阅逐笔数据后，校验逐笔数据接收情况')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() == 0)

    #   再订阅
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))

    def test_UnQuoteTradeData_Msg_04(self):
        """ 订阅多个市场，取消订阅时部分合约代码与订阅时的不一致"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        exchange1 = 'CME'
        code1 = '6S2006'
        code2 = 'E72006'
        code3 = 'J7main'
        code4 = 'NQmain'
        code5 = 'MNQmain'
        code6 = 'ESmain'
        exchange2 = 'NYMEX'
        code7 = 'CLmain'
        code8 = 'QM2007'
        code9 = 'NG2007'
        code10 = 'BZ2007'
        exchange3 = 'CBOT'
        code11 = 'ZBmain'
        code12 = 'ZCmain'
        code13 = 'ZSmain'
        code14 = 'xxxx'
        base_info = [{'exchange': exchange1, 'code': code1}, {'exchange': exchange1, 'code': code2},
                     {'exchange': exchange1, 'code': code3}, {'exchange': exchange1, 'code': code4},
                     {'exchange': exchange1, 'code': code5}, {'exchange': exchange1, 'code': code6},
                     {'exchange': exchange2, 'code': code7}, {'exchange': exchange2, 'code': code8},
                     {'exchange': exchange2, 'code': code9}, {'exchange': exchange2, 'code': code10},
                     {'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                     {'exchange': exchange3, 'code': code13}]
        base_info2 = [{'exchange': exchange3, 'code': code11}, {'exchange': exchange3, 'code': code12},
                      {'exchange': exchange3, 'code': code13}, {'exchange': exchange3, 'code': code14}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_TRADE_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2, exchange3))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10, code11, code12, code13))
        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info2,
                                                recv_num=20, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retMsg') == "unsubscribe success")
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retMsg') == "instrument code [ {} ] is unknown".format(code14))
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for i in range(info_list.__len__()):
            info = info_list[i]
            self.assertTrue(self.common.searchDicKV(info, 'exchange') in (exchange1, exchange2))
            self.assertTrue(
                self.common.searchDicKV(info, 'instrCode') in (code1, code2, code3, code4, code5, code6, code7,
                                                               code8, code9, code10))


    # --------------------------------------------订阅品种交易状态------------------------------------------------
    # 查询品种交易状态
    def test_TradeStatusMsgApi_01(self):

        start_time_stamp = int(time.time() * 1000)
        exchange = 'HKFE'
        product_list = []
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeStatusMsgReqApi(exchange=exchange, productList=product_list))

        self.logger.debug(u'通过查询接口，获取查询结果信息')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retResult') == 'SUCCESS')

        self.logger.debug(u'通过品种交易状态的接口，接收交易状态数据，并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushTradeStatusDataApi(recv_num=10))
        self.assertTrue(self.common.searchDicKV(info_list, 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(info_list, 'productCode') in product_list)




# # 开始请求分时页面数据StartChartDataReq
# def test_StartCharDataReq_001(self):
#     """
#     开始请求分时页面数据StartChartDataReq
#     """
#     exchange = 'HKFE'
#     code = 'HHI2006'
#     frequency = '2'
#     start_time_stamp = int(time.time() * 1000)
#     start_time = int(time.time() * 1000)
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_time, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     before_appbasic_json_list = rsp_list['before_appbasic_json_list']
#     before_appsnapshot_json_list = rsp_list['before_appsnapshot_json_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
#
#     self.logger.debug(u'校验最近一笔app静态数据值')
#     inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', before_appbasic_json_list)
#     self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
#
#     self.logger.debug(u'校验最近一笔app快照数据值')
#     inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_appsnapshot_json_list, is_before_snapshot=True, sub_time=start_time_stamp)
#     self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
#
#     self.logger.debug(u'通过接收快照数据的接口，筛选出app快照数据,并校验')
#
#     info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=20))
#     inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, sub_time=start_time_stamp)
#     self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
#
#     self.logger.debug(u'通过接收盘口数据的接口，筛选出app盘口数据,并校验')
#     info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=20))
#     inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list, start_sub_time=start_time_stamp)
#     self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
#
#     self.logger.debug(u'通过接收盘口数据的接口，筛选出app静态数据,并校验')
#     info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=20))
#     self.assertTrue(info_list.__len__() == 0)
#
#     self.logger.debug(u'通过接收逐笔数据的接口，筛选出app逐笔数据,并校验')
#     info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=20))
#     inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list, start_sub_time=start_time_stamp)
#     self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
#
# # 开始请求分时页面数据StartChartDataReq不传exchange
# def test_StartCharDataReq_002(self):
#     """
#     开始请求分时页面数据StartChartDataReq不传exchange
#     """
#     exchange = ''
#     code = 'HHI2006'
#     frequency = '2'
#     start_time_stamp = int(time.time() * 1000)
#     start_time = int(time.time() * 1000)
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_time, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'exchange入参错误')
#
# # 开始请求分时页面数据StartChartDataReq传错误exchange
# def test_StartCharDataReq_003(self):
#     """
#     开始请求分时页面数据StartChartDataReq传错误exchange
#     """
#     exchange = 'HI'
#     code = 'HHI2006'
#     frequency = '2'
#     start_time_stamp = int(time.time() * 1000)
#     start_time = int(time.time() * 1000)
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_time, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'exchange入参错误')
#
# # 开始请求分时页面数据StartChartDataReq不传code
# def test_StartCharDataReq_004(self):
#     """
#     开始请求分时页面数据StartChartDataReq不传code
#     """
#     exchange = 'HKFE'
#     code = ''
#     frequency = '2'
#     start_time_stamp = int(time.time() * 1000)
#     start_time = int(time.time() * 1000)
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_time, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'code入参错误')
#
# # 开始请求分时页面数据StartChartDataReq传错误code
# def test_StartCharDataReq_005(self):
#     """
#     开始请求分时页面数据StartChartDataReq传错误code
#     """
#     exchange = 'HKFE'
#     code = '0202'
#     frequency = '2'
#     start_time_stamp = int(time.time() * 1000)
#     start_time = int(time.time() * 1000)
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_time, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'code入参错误')
#
# # 开始请求分时页面数据StartChartDataReq不传frequency
# def test_StartCharDataReq_006(self):
#     """
#     开始请求分时页面数据StartChartDataReq不传frequency
#     """
#     exchange = 'HKFE'
#     code = 'HHI2006'
#     frequency = ''
#     start_time_stamp = int(time.time() * 1000)
#     start_time = int(time.time() * 1000)
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_time, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'frequency入参错误')
#
# # 开始请求分时页面数据StartChartDataReq传非法frequency
# def test_StartCharDataReq_007(self):
#     """
#     开始请求分时页面数据StartChartDataReq传非法frequency
#     """
#     exchange = 'HKFE'
#     code = 'HHI2006'
#     frequency = 'X'
#     start_time_stamp = int(time.time() * 1000)
#     start_time = int(time.time() * 1000)
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_time, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'frequency入参错误')
#
# # 开始请求分时页面数据StartChartDataReq不传start_time
# def test_StartCharDataReq_008(self):
#     """
#     开始请求分时页面数据StartChartDataReq不传start_time
#     """
#     exchange = 'HKFE'
#     code = 'HHI2006'
#     frequency = '2'
#     start_time_stamp = int(time.time() * 1000)
#     start_time = ''
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_time, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'start_time入参错误')
#
# # 开始请求分时页面数据StartChartDataReq传错误start_time
# def test_StartCharDataReq_009(self):
#     """
#     开始请求分时页面数据StartChartDataReq传错误start_time
#     """
#     exchange = 'HKFE'
#     code = 'HHI2006'
#     frequency = '2'
#     start_time_stamp = int(time.time() * 1000)
#     start_time = int(time.time() * 1000) + 1
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_time, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'start_time入参错误')
#
# # 开始请求分时页面数据StartChartDataReq传错误start_time_stamp
# def test_StartCharDataReq_010(self):
#     """
#     开始请求分时页面数据StartChartDataReq传错误start_time_stamp
#     """
#     exchange = 'HKFE'
#     code = 'HHI2006'
#     frequency = '2'
#     start_time_stamp = int(time.time() * 1000) + 1
#     start_time = int(time.time() * 1000)
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_time, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'start_time_stamp入参错误')
#
# # 开始请求分时页面数据StartChartDataReq不传start_time_stamp
# def test_StartCharDataReq_011(self):
#     """
#     开始请求分时页面数据StartChartDataReq不传start_time_stamp
#     """
#     exchange = 'HKFE'
#     code = 'HHI2006'
#     frequency = '2'
#     start_time_stamp = ''
#     start_time = int(time.time() * 1000) + 1
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_time, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'start_time入参错误')
#
# # 停止请求分时页面数据StopChartDataReqApi
# def test_StopChartDataReqApi_001(self):
#     """
#     停止请求分时页面数据StopChartDataReqApi
#     """
#     exchange = 'HKFE'
#     code = 'HHI2006'
#     frequency = '2'
#     start_time_stamp = int(time.time() * 1000)
#     start_date = int(time.time() * 1000)
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_date, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
#
#     start_time_stamp = int(time.time() * 1000)
#     exchange = 'HKFE'
#     code = 'HHI2006'
#
#     self.logger.debug(u'通过调用取消请求分时页面接口，取消APP分时数据，并检查返回结果')
#     first_rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StopChartDataReqApi(exchange, code, start_time_stamp))
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
#
#     self.logger.debug(u'通过停止请求分时页面数据的接口，取消APP分时数据，筛选是否会返回静态数据,并校验')
#     rsp_info = asyncio.get_event_loop().run_until_complete(
#         future=self.api.QuoteBasicInfoApi(recv_num=10))
#     self.assertTrue(len(rsp_info) == 0)
#
#     self.logger.debug(u'通过停止请求分时页面数据的接口，取消APP分时数据，筛选是否返回出快照数据,并校验')
#     rsp_info = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=10))
#     self.assertTrue(rsp_info.__len__() == 0)
#
#     self.logger.debug(u'通过停止请求分时页面数据的接口，取消APP分时数据，筛选是否返回出静态数据,并校验')
#     rsp_info = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=10))
#     self.assertTrue(rsp_info.__len__() == 0)
#
#     self.logger.debug(u'通过停止请求分时页面数据的接口，取消APP分时数据，筛选出是否返回盘口数据,并校验')
#     rsp_info = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=10))
#     self.assertTrue(rsp_info.__len__() == 0)
#
#     self.logger.debug(u'通过停止请求分时页面数据的接口，取消APP分时数据，筛选出是否返回逐笔数据,并校验')
#     rsp_info = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=10))
#     self.assertTrue(rsp_info.__len__() == 0)
#
# # 停止请求分时页面数据StopChartDataReqApi不传exchange
# def test_StopChartDataReqApi_002(self):
#     """
#     停止请求分时页面数据StopChartDataReqApi不传exchange
#     """
#     exchange = 'HKFE'
#     code = 'HHI2006'
#     frequency = '2'
#     start_time_stamp = int(time.time() * 1000)
#     start_date = int(time.time() * 1000)
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_date, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
#
#     start_time_stamp = int(time.time() * 1000)
#     exchange = ''
#     code = 'HHI2006'
#
#     self.logger.debug(u'通过调用取消请求分时页面接口，取消APP分时数据，并检查返回结果')
#     first_rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StopChartDataReqApi(exchange, code, start_time_stamp))
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'exchange入参错误')
#
# # 停止请求分时页面数据StopChartDataReqApi传错误exchange
# def test_StopChartDataReqApi_003(self):
#     """
#     停止请求分时页面数据StopChartDataReqApi传错误exchange
#     """
#     exchange = 'HKFE'
#     code = 'HHI2006'
#     frequency = '2'
#     start_time_stamp = int(time.time() * 1000)
#     start_date = int(time.time() * 1000)
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_date, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
#
#     start_time_stamp = int(time.time() * 1000)
#     exchange = 'XX'
#     code = 'HHI2006'
#
#     self.logger.debug(u'通过调用取消请求分时页面接口，取消APP分时数据，并检查返回结果')
#     first_rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StopChartDataReqApi(exchange, code, start_time_stamp))
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'exchange入参错误')
#
# # 停止请求分时页面数据StopChartDataReqApi传错误code
# def test_StopChartDataReqApi_004(self):
#     """
#     停止请求分时页面数据StopChartDataReqApi传错误code
#     """
#     exchange = 'HKFE'
#     code = 'HHI2006'
#     frequency = '2'
#     start_time_stamp = int(time.time() * 1000)
#     start_date = int(time.time() * 1000)
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_date, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
#
#     start_time_stamp = int(time.time() * 1000)
#     exchange = 'HKFE'
#     code = 'XX2006'
#
#     self.logger.debug(u'通过调用取消请求分时页面接口，取消APP分时数据，并检查返回结果')
#     first_rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StopChartDataReqApi(exchange, code, start_time_stamp))
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'code入参错误')
#
# # 停止请求分时页面数据StopChartDataReqApi不传code
# def test_StopChartDataReqApi_005(self):
#     """
#     停止请求分时页面数据StopChartDataReqApi不传code
#     """
#     exchange = 'HKFE'
#     code = 'HHI2006'
#     frequency = '2'
#     start_time_stamp = int(time.time() * 1000)
#     start_date = int(time.time() * 1000)
#
#     self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
#     asyncio.get_event_loop().run_until_complete(
#         future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
#     rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StartChartDataReqApi(exchange, code, frequency, start_date, start_time_stamp))
#     first_rsp_list = rsp_list['first_app_rsp_list']
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
#
#     start_time_stamp = int(time.time() * 1000)
#     exchange = 'HKFE'
#     code = ''
#
#     self.logger.debug(u'通过调用取消请求分时页面接口，取消APP分时数据，并检查返回结果')
#     first_rsp_list = asyncio.get_event_loop().run_until_complete(
#         future=self.api.StopChartDataReqApi(exchange, code, start_time_stamp))
#     self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'code入参错误')


if __name__ == '__main_':
    unittest.main()
