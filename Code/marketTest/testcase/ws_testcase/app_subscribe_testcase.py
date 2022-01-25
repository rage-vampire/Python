# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/6/2
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

    def inner_zmq_test_case(self, case_name, check_json_list, is_before_data=False, start_sub_time=None, start_time=None, exchange=None, instr_code=None, peroid_type=None):
        suite = unittest.TestSuite()
        suite.addTest(CheckZMQ(case_name))
        suite._tests[0].check_json_list = check_json_list
        suite._tests[0].is_before_data = is_before_data
        suite._tests[0].sub_time = start_sub_time
        suite._tests[0].start_time = start_time
        suite._tests[0].exchange = exchange
        suite._tests[0].instr_code = instr_code
        suite._tests[0].peroid_type = peroid_type

        runner = unittest.TextTestRunner()
        inner_test_result = runner.run(suite)
        return inner_test_result

    # ------------------------------------------登录-----------------------------------------------------------
    def test_LoginReq01(self):
        """正常登陆"""
        start_time_stamp = int(time.time() * 1000)
        frequence = 4
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接受时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')))

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
    #
    # # -------------------------------------------------------测速-------------------------------------------------------
    def test_VelocityReqApi01(self):
        start_time_stamp = int(time.time() * 1000)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.VelocityReqApi(start_time=start_time_stamp))

        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTime')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'sendTime')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvTime')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTime')))





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

# --------------------------------------------------订阅start-------------------------------------------------------
# --------------------------------------------------开始请求分时页面数据-------------------------------------------------------

    def test_StartCharDataReq_001(self):
        """分时页面请求订阅一个合约，frequence=4，start_time为5分钟前"""
        exchange = 'HKFE'
        code = 'HHI2006'
        frequence = 4
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 - 5 * 60 * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(app_rsp['code'] == code)
        self.assertTrue(app_rsp['exchange'] == 'HKFE')
        basic_json_list = [app_rsp['basicData']]
        before_snapshot_json_list = [app_rsp['snapshot']]
        before_orderbook_json_list = [app_rsp['orderbook']]
        before_klineMin_json_list = app_rsp['klineMin']
        before_tradeData_json_list = app_rsp['tradeData']
        self.logger.debug(u'校验静态数据值')
        self.assertTrue(basic_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in basic_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in before_snapshot_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in before_orderbook_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
        self.logger.debug(u'校验前逐笔数据')
        self.assertTrue(before_tradeData_json_list.__len__() > 0)
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', before_tradeData_json_list, is_before_data=True, start_sub_time=start_time_stamp, start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in before_tradeData_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
        self.logger.debug(u'校验前分时数据')
        self.assertTrue(before_klineMin_json_list.__len__() > 0)
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', before_klineMin_json_list, is_before_data=True, start_sub_time=start_time_stamp, start_time=start_time, exchange=exchange, instr_code=code)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=50))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=50))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推逐笔数据

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推分时数据

    def test_StartCharDataReq_002(self):
        """分时页面请求订阅一个合约，frequence=0(当成1处理)，start_time为5分钟前"""
        exchange = 'HKFE'
        code = 'HHI2006'
        frequence = 0
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 - 5 * 60 * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(self.common.searchDicKV(app_rsp, 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(app_rsp, 'code') == code)
        basic_json_list = [app_rsp['basicData']]
        before_snapshot_json_list = [app_rsp['snapshot']]
        before_orderbook_json_list = [app_rsp['orderbook']]
        before_klineMin_json_list = app_rsp['klineMin']
        before_tradeData_json_list = app_rsp['tradeData']
        self.logger.debug(u'校验静态数据值')
        self.assertTrue(basic_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前逐笔数据')
        self.assertTrue(before_tradeData_json_list.__len__() > 0)
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', before_tradeData_json_list, is_before_data=True, start_sub_time=start_time_stamp, start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前分时数据')
        self.assertTrue(before_klineMin_json_list.__len__() > 0)
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', before_klineMin_json_list, is_before_data=True, start_sub_time=start_time_stamp, start_time=start_time, exchange=exchange, instr_code=code)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=50))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=50))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推逐笔数据

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推分时数据

    def test_StartCharDataReq_003(self):
        """分时页面请求订阅一个合约，frequence=None(当成1处理)，start_time为5分钟前"""
        exchange = 'HKFE'
        code = 'HHI2006'
        frequence = None
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 - 5 * 60 * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(self.common.searchDicKV(app_rsp, 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(app_rsp, 'code') == code)
        basic_json_list = [app_rsp['basicData']]
        before_snapshot_json_list = [app_rsp['snapshot']]
        before_orderbook_json_list = [app_rsp['orderbook']]
        before_klineMin_json_list = app_rsp['klineMin']
        before_tradeData_json_list = app_rsp['tradeData']
        self.logger.debug(u'校验静态数据值')
        self.assertTrue(basic_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前逐笔数据')
        self.assertTrue(before_tradeData_json_list.__len__() > 0)
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', before_tradeData_json_list, is_before_data=True, start_sub_time=start_time_stamp, start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前分时数据')
        self.assertTrue(before_klineMin_json_list.__len__() > 0)
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', before_klineMin_json_list, is_before_data=True, start_sub_time=start_time_stamp, start_time=start_time, exchange=exchange, instr_code=code)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=50))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=50))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推逐笔数据

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推分时数据

    def test_StartCharDataReq_004(self):
        """分时页面请求订阅一个合约，frequence=100，start_time为5分钟前"""
        exchange = 'HKFE'
        code = 'HHI2006'
        frequence = 100
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 - 5 * 60 * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(self.common.searchDicKV(app_rsp, 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(app_rsp, 'code') == code)
        basic_json_list = [app_rsp['basicData']]
        before_snapshot_json_list = [app_rsp['snapshot']]
        before_orderbook_json_list = [app_rsp['orderbook']]
        before_klineMin_json_list = app_rsp['klineMin']
        before_tradeData_json_list = app_rsp['tradeData']
        self.logger.debug(u'校验静态数据值')
        self.assertTrue(basic_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前逐笔数据')
        self.assertTrue(before_tradeData_json_list.__len__() > 0)
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', before_tradeData_json_list, is_before_data=True, start_sub_time=start_time_stamp, start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前分时数据')
        self.assertTrue(before_klineMin_json_list.__len__() > 0)
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', before_klineMin_json_list, is_before_data=True, start_sub_time=start_time_stamp, start_time=start_time, exchange=exchange, instr_code=code)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=50))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=50))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推逐笔数据

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推分时数据

    def test_StartCharDataReq_005(self):
        """分时页面请求订阅一个合约，frequence=100，start_time为7天前"""
        exchange = 'HKFE'
        code = 'HHI2006'
        frequence = 100
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 - 7 * 24 * 60 * 60 * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(self.common.searchDicKV(app_rsp, 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(app_rsp, 'code') == code)
        basic_json_list = [app_rsp['basicData']]
        before_snapshot_json_list = [app_rsp['snapshot']]
        before_orderbook_json_list = [app_rsp['orderbook']]
        before_klineMin_json_list = app_rsp['klineMin']
        before_tradeData_json_list = app_rsp['tradeData']

        self.logger.debug(u'校验静态数据值')
        self.assertTrue(basic_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前逐笔数据')
        self.assertTrue(before_tradeData_json_list.__len__() > 0)
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', before_tradeData_json_list, is_before_data=True, start_sub_time=start_time_stamp, start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前分时数据')
        self.assertTrue(before_klineMin_json_list.__len__() > 0)
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', before_klineMin_json_list, is_before_data=True, start_sub_time=start_time_stamp, start_time=start_time, exchange=exchange, instr_code=code)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=50))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=50))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推逐笔数据

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推分时数据

    def test_StartCharDataReq_006(self):
        """分时页面请求订阅一个合约，frequence=100，start_time为当前时间"""
        exchange = 'HKFE'
        code = 'HHI2006'
        frequence = 100
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(self.common.searchDicKV(app_rsp, 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(app_rsp, 'code') == code)
        basic_json_list = [app_rsp['basicData']]
        before_snapshot_json_list = [app_rsp['snapshot']]
        before_orderbook_json_list = [app_rsp['orderbook']]
        self.assertTrue('klineMin' not in app_rsp.keys())
        self.assertTrue('tradeData' not in app_rsp.keys())
        self.logger.debug(u'校验静态数据值')
        self.assertTrue(basic_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=50))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=50))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推逐笔数据

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推分时数据

    def test_StartCharDataReq_007(self):
        """分时页面请求订阅一个合约，frequence=100，start_time为未来时间"""
        exchange = 'HKFE'
        code = 'HHI2006'
        frequence = 100
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 + 1000000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(self.common.searchDicKV(app_rsp, 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(app_rsp, 'code') == code)
        basic_json_list = [app_rsp['basicData']]
        before_snapshot_json_list = [app_rsp['snapshot']]
        before_orderbook_json_list = [app_rsp['orderbook']]
        self.assertTrue('klineMin' not in app_rsp.keys())
        self.assertTrue('tradeData' not in app_rsp.keys())
        self.logger.debug(u'校验静态数据值')
        self.assertTrue(basic_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list, is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=50))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=50))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推逐笔数据

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推分时数据

    def test_StartCharDataReq_008(self):
        """分时页面请求订阅一个合约，frequence=100，start_time为5分钟前,再订阅第二个合约"""
        exchange = 'HKFE'
        code1 = 'HHI2006'
        code2 = 'HSI2006'
        frequence = 100
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 - 5 * 60 * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code1, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(app_rsp['code'] == code1)
        self.assertTrue(app_rsp['exchange'] == 'HKFE')
        basic_json_list = [app_rsp['basicData']]
        before_snapshot_json_list = [app_rsp['snapshot']]
        before_orderbook_json_list = [app_rsp['orderbook']]
        before_klineMin_json_list = app_rsp['klineMin']
        before_tradeData_json_list = app_rsp['tradeData']
        self.logger.debug(u'校验静态数据值')
        self.assertTrue(basic_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in basic_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in before_snapshot_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
        self.logger.debug(u'校验前盘口数据')
        self.assertTrue(before_orderbook_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in before_orderbook_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
        self.logger.debug(u'校验前逐笔数据')
        self.assertTrue(before_tradeData_json_list.__len__() > 0)
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', before_tradeData_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp,
                                                     start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in before_tradeData_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
        self.logger.debug(u'校验前分时数据')
        self.assertTrue(before_klineMin_json_list.__len__() > 0)
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', before_klineMin_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp,
                                                     start_time=start_time, exchange=exchange, instr_code=code1)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果2')
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 - 5 * 60 * 1000)
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code2, start_time, start_time_stamp, recv_num=100))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(app_rsp['code'] == code2)
        self.assertTrue(app_rsp['exchange'] == 'HKFE')
        basic_json_list = [app_rsp['basicData']]
        before_snapshot_json_list = [app_rsp['snapshot']]
        before_orderbook_json_list = [app_rsp['orderbook']]
        before_klineMin_json_list = app_rsp['klineMin']
        before_tradeData_json_list = app_rsp['tradeData']
        self.logger.debug(u'校验静态数据值2')
        self.assertTrue(basic_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_03_QuoteBasicInfo', basic_json_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in basic_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code2)
        self.logger.debug(u'校验前快照数据2')
        self.assertTrue(before_snapshot_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', before_snapshot_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in before_snapshot_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code2)
        self.logger.debug(u'校验前盘口数据2')
        self.assertTrue(before_orderbook_json_list.__len__() == 1)
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', before_orderbook_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in before_orderbook_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code2)
        self.logger.debug(u'校验前逐笔数据2')
        self.assertTrue(before_tradeData_json_list.__len__() > 0)
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', before_tradeData_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp,
                                                     start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in before_tradeData_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code2)
        self.logger.debug(u'校验前分时数据2')
        self.assertTrue(before_klineMin_json_list.__len__() > 0)
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', before_klineMin_json_list,
                                                     is_before_data=True, start_sub_time=start_time_stamp,
                                                     start_time=start_time, exchange=exchange, instr_code=code2)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)


        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_01_QuoteSnapshot', info_list,
                                                     start_sub_time=start_time_stamp)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        recv_code_list = []
        for info in info_list:
            recv_code_list.append(self.common.searchDicKV(info, 'instrCode'))
        self.assertTrue(set(recv_code_list) == {code1, code2})

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_02_QuoteOrderBookData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        recv_code_list = []
        for info in info_list:
            recv_code_list.append(self.common.searchDicKV(info, 'instrCode'))
        self.assertTrue(set(recv_code_list) == {code1, code2})

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)  # 不主推逐笔数据

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)  # 不主推分时数据

    def test_StartCharDataReq_009(self):
        """exchange传入Unknown"""
        exchange = 'UNKNOWN'
        code = 'HHI2005'
        frequence = 100
        start_time_stamp = int(time.time() * 1000 - 100000)
        start_time = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code))
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(self.common.searchDicKV(app_rsp, 'code') == code)
        self.assertTrue('basicData' not in app_rsp.keys())
        self.assertTrue('snapshot' not in app_rsp.keys())
        self.assertTrue('orderbook' not in app_rsp.keys())
        self.assertTrue('klineMin' not in app_rsp.keys())
        self.assertTrue('tradeData' not in app_rsp.keys())

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推逐笔数据

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推分时数据

    def test_StartCharDataReq_010(self):
        """不传code"""
        exchange = 'HKFE'
        code = ''
        frequence = 100
        start_time_stamp = int(time.time() * 1000 - 100000)
        start_time = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retMsg') == 'instr [ {} ] error'.format(exchange))
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(self.common.searchDicKV(app_rsp, 'exchange') == exchange)
        self.assertTrue('basicData' not in app_rsp.keys())
        self.assertTrue('snapshot' not in app_rsp.keys())
        self.assertTrue('orderbook' not in app_rsp.keys())
        self.assertTrue('klineMin' not in app_rsp.keys())
        self.assertTrue('tradeData' not in app_rsp.keys())

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推逐笔数据

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推分时数据

    def test_StartCharDataReq_011(self):
        """传错误code"""
        exchange = 'HKFE'
        code = 'HHI2005'    # HHI2005已下架
        frequence = 100
        start_time_stamp = int(time.time() * 1000 - 100000)
        start_time = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code))
        self.assertTrue(self.common.searchDicKV(app_rsp, 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(app_rsp, 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue('basicData' not in app_rsp.keys())
        self.assertTrue('snapshot' not in app_rsp.keys())
        self.assertTrue('orderbook' not in app_rsp.keys())
        self.assertTrue('klineMin' not in app_rsp.keys())
        self.assertTrue('tradeData' not in app_rsp.keys())

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推逐笔数据

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推分时数据

    def test_StartCharDataReq_012(self):
        """传start_time为None"""
        exchange = 'HKFE'
        code = 'HHI2006'
        frequence = 100
        start_time_stamp = int(time.time() * 1000 - 100000)
        start_time = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retMsg') == 'start time is empty'.format(start_time))
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(self.common.searchDicKV(app_rsp, 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(app_rsp, 'code') == code)
        self.assertTrue('basicData' not in app_rsp.keys())
        self.assertTrue('snapshot' not in app_rsp.keys())
        self.assertTrue('orderbook' not in app_rsp.keys())
        self.assertTrue('klineMin' not in app_rsp.keys())
        self.assertTrue('tradeData' not in app_rsp.keys())

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推逐笔数据

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)  # 不主推分时数据

# --------------------------------------------------停止请求分时页面数据-------------------------------------------------------
    def test_StopChartDataReqApi_001(self):
        """订阅一个合约,停止请求分时页面数据"""
        exchange = 'HKFE'
        code = 'HHI2006'
        frequence = 100
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 - 5 * 60 * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        start_time_stamp = int(time.time() * 1000)
        self.logger.debug(u'取消订阅分时页面数据')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StopChartDataReqApi(exchange, code, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(app_rsp['code'] == code)
        self.assertTrue(app_rsp['exchange'] == 'HKFE')
        self.logger.debug(u'通过接收所有数据的返回,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.AppQuoteAllApi(recv_num=200))
        self.assertTrue(info_list.__len__() == 0)

    def test_StopChartDataReqApi_002(self):
        """订阅2个合约,停止请求其中一个的分时页面数据"""
        exchange = 'HKFE'
        code1 = 'HHI2006'
        code2 = 'HSI2006'
        frequence = 100
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 - 5 * 60 * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code1, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code2, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.logger.debug(u'取消订阅分时页面数据')
        start_time_stamp = int(time.time() * 1000)
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StopChartDataReqApi(exchange, code1, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(app_rsp['code'] == code1)
        self.assertTrue(app_rsp['exchange'] == 'HKFE')

        self.logger.debug(u'通过接收所有数据的返回,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.AppQuoteAllApi(recv_num=50))
        self.assertTrue(info_list.__len__() > 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code2)

    def test_StopChartDataReqApi_003(self):
        """订阅2个合约,停止请求2个的分时页面数据"""
        exchange = 'HKFE'
        code1 = 'HHI2006'
        code2 = 'HSI2006'
        frequence = 100
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 - 5 * 60 * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code1, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code2, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.logger.debug(u'取消订阅分时页面数据')
        start_time_stamp = int(time.time() * 1000)
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StopChartDataReqApi(exchange, code1, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(app_rsp['code'] == code1)
        self.assertTrue(app_rsp['exchange'] == 'HKFE')

        start_time_stamp = int(time.time() * 1000)
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StopChartDataReqApi(exchange, code2, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(app_rsp['code'] == code2)
        self.assertTrue(app_rsp['exchange'] == 'HKFE')
        self.logger.debug(u'通过接收所有数据的返回,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.AppQuoteAllApi(recv_num=50))
        self.assertTrue(info_list.__len__() == 0)

    def test_StopChartDataReqApi_004(self):
        """停止请求分时页面数据,exchange传入UNKNOWN"""
        exchange = 'HKFE'
        exchange2 = 'UNKNOWN'
        code = 'HHI2006'
        frequence = 100
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 - 5 * 60 * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        start_time_stamp = int(time.time() * 1000)
        self.logger.debug(u'取消订阅分时页面数据')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StopChartDataReqApi(exchange2, code, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retMsg') == 'instr [ {}_{} ] error'.format(exchange2, code))
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(app_rsp['code'] == code)
        self.logger.debug(u'通过接收所有数据的返回,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.AppQuoteAllApi(recv_num=50))
        self.assertTrue(info_list.__len__() > 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    def test_StopChartDataReqApi_005(self):
        """停止请求分时页面数据,exchange传入None"""
        exchange = 'HKFE'
        exchange2 = None
        code = 'HHI2006'
        frequence = 100
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 - 5 * 60 * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        start_time_stamp = int(time.time() * 1000)
        self.logger.debug(u'取消订阅分时页面数据')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StopChartDataReqApi(exchange2, code, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retMsg') == 'instr [ UNKNOWN_{} ] error'.format(code))
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(app_rsp['code'] == code)
        self.logger.debug(u'通过接收所有数据的返回,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.AppQuoteAllApi(recv_num=50))
        self.assertTrue(info_list.__len__() > 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    def test_StopChartDataReqApi_006(self):
        """停止请求分时页面数据,code传入未订阅的code"""
        exchange = 'HKFE'
        code = 'HHI2006'
        code2 = 'xxxx'
        frequence = 100
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 - 5 * 60 * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        start_time_stamp = int(time.time() * 1000)
        self.logger.debug(u'取消订阅分时页面数据')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StopChartDataReqApi(exchange, code2, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code2))
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(app_rsp['code'] == code2)
        self.assertTrue(app_rsp['exchange'] == 'HKFE')
        self.logger.debug(u'通过接收所有数据的返回,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.AppQuoteAllApi(recv_num=50))
        self.assertTrue(info_list.__len__() > 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    def test_StopChartDataReqApi_007(self):
        """停止请求分时页面数据,code传入未订阅的code"""
        exchange = 'HKFE'
        code = 'HHI2006'
        code2 = 'HSI2006'
        frequence = 100
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 - 5 * 60 * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        start_time_stamp = int(time.time() * 1000)
        self.logger.debug(u'取消订阅分时页面数据')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StopChartDataReqApi(exchange, code2, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retMsg') == 'instr have no start')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(app_rsp['code'] == code2)
        self.assertTrue(app_rsp['exchange'] == 'HKFE')
        self.logger.debug(u'通过接收所有数据的返回,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.AppQuoteAllApi(recv_num=50))
        self.assertTrue(info_list.__len__() > 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    def test_StopChartDataReqApi_008(self):
        """停止请求分时页面数据,code传入不存在的code"""
        exchange = 'HKFE'
        code = 'HHI2006'
        code2 = 'xxxx'
        frequence = 100
        start_time_stamp = int(time.time() * 1000)
        start_time = int(time.time() * 1000 - 5 * 60 * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'通过调用请求分时页面数据接口，订阅数据，并检查返回结果')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StartChartDataReqApi(exchange, code, start_time, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        start_time_stamp = int(time.time() * 1000)
        self.logger.debug(u'取消订阅分时页面数据')
        app_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.StopChartDataReqApi(exchange, code2, start_time_stamp))
        self.assertTrue(app_rsp_list.__len__() == 1)
        app_rsp = app_rsp_list[0]
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(app_rsp, 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code2))
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于开始测速时间
        self.assertTrue(int(self.common.searchDicKV(app_rsp, 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(app_rsp, 'startTimeStamp')))
        self.assertTrue(app_rsp['code'] == code2)
        self.assertTrue(app_rsp['exchange'] == 'HKFE')
        self.logger.debug(u'通过接收所有数据的返回,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.AppQuoteAllApi(recv_num=50))
        self.assertTrue(info_list.__len__() > 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

# --------------------------------------------------逐笔成交查询-------------------------------------------------------
    def test_QueryTradeTickMsgReqApi_001(self):
        """逐笔成交查询: BY_DATE_TIME,与当前时间间隔5分钟, isSubTrade = True, frequence=2"""
        frequence = 2
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp - 5 * 60 * 1000
        end_time = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验回包里的历史逐笔数据')
        tick_data_list = self.common.searchDicKV(query_trade_tick_rsp_list[0], 'tickData')
        inner_test_result = self.inner_zmq_test_case('test_04_APP_BeforeQuoteTradeData', tick_data_list, start_sub_time=end_time, start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    def test_QueryTradeTickMsgReqApi_002(self):
        """逐笔成交查询: BY_DATE_TIME,与当前时间间隔5分钟, isSubTrade = True, frequence=None"""
        frequence = None
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp - 5 * 60 * 1000
        end_time = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验回包里的历史逐笔数据')
        tick_data_list = self.common.searchDicKV(query_trade_tick_rsp_list[0], 'tickData')
        inner_test_result = self.inner_zmq_test_case('test_04_APP_BeforeQuoteTradeData', tick_data_list, start_sub_time=end_time, start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    def test_QueryTradeTickMsgReqApi_003(self):
        """逐笔成交查询: BY_DATE_TIME,与当前时间间隔5分钟, isSubTrade = False, frequence=100"""
        frequence = 100
        isSubTrade = False
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp - 5 * 60 * 1000
        end_time = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(sub_trade_tick_rsp_list.__len__() == 0)

        self.logger.debug(u'校验回包里的历史逐笔数据')
        tick_data_list = self.common.searchDicKV(query_trade_tick_rsp_list[0], 'tickData')
        inner_test_result = self.inner_zmq_test_case('test_04_APP_BeforeQuoteTradeData', tick_data_list, start_sub_time=end_time, start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryTradeTickMsgReqApi_004(self):
        """逐笔成交查询: BY_DATE_TIME,与当前时间间隔0分钟, isSubTrade = True, frequence=100"""
        frequence = 100
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp
        end_time = start_time
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retMsg') == 'query condition error')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)

        self.assertTrue(sub_trade_tick_rsp_list.__len__() == 0)

        self.logger.debug(u'校验回包里的历史逐笔数据')
        self.assertTrue('tickData' not in query_trade_tick_rsp_list[0])

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryTradeTickMsgReqApi_005(self):
        """逐笔成交查询: BY_DATE_TIME,时间间隔-5分钟, isSubTrade = True, frequence=100"""
        frequence = 100
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp - 5 * 60 * 1000
        end_time = start_time_stamp - 10 * 60 * 1000
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retMsg') == 'query condition error')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)

        self.assertTrue(sub_trade_tick_rsp_list.__len__() == 0)

        self.logger.debug(u'校验回包里的历史逐笔数据')
        self.assertTrue('tickData' not in query_trade_tick_rsp_list[0])

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryTradeTickMsgReqApi_006(self):
        """逐笔成交查询: BY_DATE_TIME,与当前时间的前10分钟-前5分钟, isSubTrade = False, frequence=100"""
        frequence = 100
        isSubTrade = False
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp - 10 * 60 * 1000
        end_time = start_time_stamp - 5 * 60 * 1000
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(sub_trade_tick_rsp_list.__len__() == 0)

        self.logger.debug(u'校验回包里的历史逐笔数据')
        tick_data_list = self.common.searchDicKV(query_trade_tick_rsp_list[0], 'tickData')
        inner_test_result = self.inner_zmq_test_case('test_04_APP_BeforeQuoteTradeData', tick_data_list, start_sub_time=end_time, start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryTradeTickMsgReqApi_007(self):
        """逐笔成交查询: BY_DATE_TIME,与当前时间间隔5分钟, isSubTrade = True, frequence=100; 订阅两个合约"""
        frequence = 100
        isSubTrade = True
        exchange = 'HKFE'
        code1 = 'HHI2006'
        code2 = 'HSI2006'
        type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp - 5 * 60 * 1000
        end_time = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code1, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code1)

        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'code') == code1)
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验回包里的历史逐笔数据')
        tick_data_list = self.common.searchDicKV(query_trade_tick_rsp_list[0], 'tickData')
        inner_test_result = self.inner_zmq_test_case('test_04_APP_BeforeQuoteTradeData', tick_data_list, start_sub_time=end_time, start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'开始订阅第二个合约:')
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp - 5 * 60 * 1000
        end_time = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code2, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code2)

        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'code') == code2)
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验回包里的历史逐笔数据')
        tick_data_list = self.common.searchDicKV(query_trade_tick_rsp_list[0], 'tickData')
        inner_test_result = self.inner_zmq_test_case('test_04_APP_BeforeQuoteTradeData', tick_data_list, start_sub_time=end_time, start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        recv_code_list = []
        for info in info_list:
            recv_code_list.append(self.common.searchDicKV(info, 'instrCode'))
        self.assertTrue(set(recv_code_list) == {code1, code2})

    def test_QueryTradeTickMsgReqApi_008(self):
        """逐笔成交查询: BY_VOL,direct=WITH_FRONT, vol=100,起始时间为当前时间, isSubTrade = True, frequence=100"""
        frequence = 100
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp
        end_time = None
        vol = 100
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验回包里的历史逐笔数据')
        tick_data_list = self.common.searchDicKV(query_trade_tick_rsp_list[0], 'tickData')
        self.assertTrue(tick_data_list.__len__() == vol)
        inner_test_result = self.inner_zmq_test_case('test_04_APP_BeforeQuoteTradeData', tick_data_list, start_sub_time=start_time, start_time=0)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    def test_QueryTradeTickMsgReqApi_009(self):
        """逐笔成交查询: BY_VOL,direct=WITH_FRONT, vol=100,起始时间为当前时间, isSubTrade = False, frequence=100"""
        frequence = 100
        isSubTrade = False
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp
        end_time = None
        vol = 100
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(final_rsp['sub_trade_tick_rsp_list'].__len__() == 0)
        self.logger.debug(u'校验回包里的历史逐笔数据')
        tick_data_list = self.common.searchDicKV(query_trade_tick_rsp_list[0], 'tickData')
        self.assertTrue(tick_data_list.__len__() == vol)
        inner_test_result = self.inner_zmq_test_case('test_04_APP_BeforeQuoteTradeData', tick_data_list, start_sub_time=start_time, start_time=0)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryTradeTickMsgReqApi_010(self):
        """逐笔成交查询: BY_VOL,direct=WITH_FRONT, vol=100,起始时间为过去5分钟, isSubTrade = True, frequence=100"""
        frequence = 100
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp - 5 * 60 * 1000
        end_time = None
        vol = 100
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验回包里的历史逐笔数据')
        tick_data_list = self.common.searchDicKV(query_trade_tick_rsp_list[0], 'tickData')
        self.assertTrue(tick_data_list.__len__() == vol)
        inner_test_result = self.inner_zmq_test_case('test_04_APP_BeforeQuoteTradeData', tick_data_list, start_sub_time=start_time, start_time=0)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    def test_QueryTradeTickMsgReqApi_011(self):
        """逐笔成交查询: BY_VOL,direct=WITH_FRONT, vol=100,起始时间为未来10分钟, isSubTrade = True, frequence=100"""
        frequence = 100
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp + 10 * 60 * 1000
        end_time = None
        vol = 100
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验回包里的历史逐笔数据')
        tick_data_list = self.common.searchDicKV(query_trade_tick_rsp_list[0], 'tickData')
        self.assertTrue(tick_data_list.__len__() == vol)
        inner_test_result = self.inner_zmq_test_case('test_04_APP_BeforeQuoteTradeData', tick_data_list, start_sub_time=start_time, start_time=0)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    def test_QueryTradeTickMsgReqApi_012(self):
        """逐笔成交查询: BY_VOL,direct=WITH_BACK, vol=100,起始时间为过去10分钟, isSubTrade = True, frequence=100"""
        frequence = 100
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp - 10 * 60 * 1000
        end_time = None
        vol = 100
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验回包里的历史逐笔数据')
        tick_data_list = self.common.searchDicKV(query_trade_tick_rsp_list[0], 'tickData')
        self.assertTrue(tick_data_list.__len__() == vol)
        inner_test_result = self.inner_zmq_test_case('test_04_APP_BeforeQuoteTradeData', tick_data_list, start_sub_time=start_time_stamp, start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    def test_QueryTradeTickMsgReqApi_013(self):
        """逐笔成交查询: BY_VOL,direct=WITH_BACK, vol=100000,起始时间为过去1分钟, isSubTrade = True, frequence=100"""
        frequence = 100
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp - 1 * 60 * 1000
        end_time = None
        vol = 100000
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验回包里的历史逐笔数据')
        tick_data_list = self.common.searchDicKV(query_trade_tick_rsp_list[0], 'tickData')
        self.assertTrue(tick_data_list.__len__() < vol)
        inner_test_result = self.inner_zmq_test_case('test_04_APP_BeforeQuoteTradeData', tick_data_list, start_sub_time=start_time_stamp, start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    def test_QueryTradeTickMsgReqApi_014(self):
        """逐笔成交查询: BY_VOL,direct=WITH_BACK, vol=100,起始时间为未来时间, isSubTrade = True, frequence=100"""
        frequence = 100
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp + 10 * 60 * 1000
        end_time = None
        vol = 100
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验回包里的历史逐笔数据')
        self.assertTrue('tickData' not in query_trade_tick_rsp_list[0].keys())
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    def test_QueryTradeTickMsgReqApi_015(self):
        """逐笔成交查询: BY_DATE_TIME,与当前时间间隔5分钟, isSubTrade = True, frequence=100;
        再订阅第二个合约：BY_VOL,direct=WITH_FRONT, vol=100,起始时间为当前时间, isSubTrade = False, frequence=100"""
        frequence = 100
        isSubTrade = True
        isSubTrade2 = False
        exchange = 'HKFE'
        code1 = 'HSI2006'
        code2 = 'HHI2006'
        type = QueryKLineMsgType.BY_DATE_TIME
        type2 = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp - 5 * 60 * 1000
        start_time2 = start_time_stamp
        end_time = start_time_stamp
        vol = 100
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code1, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code1)

        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'code') == code1)
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'校验回包里的历史逐笔数据')
        tick_data_list = self.common.searchDicKV(query_trade_tick_rsp_list[0], 'tickData')
        inner_test_result = self.inner_zmq_test_case('test_04_APP_BeforeQuoteTradeData', tick_data_list, start_sub_time=end_time, start_time=start_time)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

        self.logger.debug(u'开始订阅第二个合约:')
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade2, exchange, code2, type2, direct, start_time2, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code2)
        self.assertTrue(sub_trade_tick_rsp_list.__len__() == 0)

        self.logger.debug(u'校验回包里的历史逐笔数据')
        tick_data_list = self.common.searchDicKV(query_trade_tick_rsp_list[0], 'tickData')
        self.assertTrue(tick_data_list.__len__() == vol)
        inner_test_result = self.inner_zmq_test_case('test_04_APP_BeforeQuoteTradeData', tick_data_list, start_sub_time=start_time2, start_time=0)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)

    def test_QueryTradeTickMsgReqApi_016(self):
        """逐笔成交查询: BY_DATE_TIME,start_time=None, isSubTrade = True, frequence=2"""
        frequence = 2
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = None
        end_time = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retMsg') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(sub_trade_tick_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryTradeTickMsgReqApi_017(self):
        """逐笔成交查询: BY_DATE_TIME,end_time=None, isSubTrade = True, frequence=2"""
        frequence = 2
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp - 10 * 60 * 1000
        end_time = None
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retMsg') == 'query condition error')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(sub_trade_tick_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryTradeTickMsgReqApi_018(self):
        """逐笔成交查询: BY_DATE_TIME,exchange=UNKNOWN, isSubTrade = True, frequence=2"""
        frequence = 2
        isSubTrade = True
        exchange = 'UNKNOWN'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp - 10 * 60 * 1000
        end_time = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code))
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(sub_trade_tick_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryTradeTickMsgReqApi_019(self):
        """逐笔成交查询: BY_DATE_TIME,code=xxxx, isSubTrade = True, frequence=2"""
        frequence = 2
        isSubTrade = True
        exchange = 'HKFE'
        code = 'xxxx'
        type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp - 10 * 60 * 1000
        end_time = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code))
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(sub_trade_tick_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryTradeTickMsgReqApi_020(self):
        """逐笔成交查询: BY_VOL,start_time=None,vol=100, direct=WITH_FRONT isSubTrade = True, frequence=2"""
        frequence = 2
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HSI2006'
        type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = None
        end_time = None
        vol = 100
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retMsg') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(sub_trade_tick_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryTradeTickMsgReqApi_021(self):
        """逐笔成交查询: BY_VOL,vol=None, direct=WITH_FRONT isSubTrade = True, frequence=2"""
        frequence = 2
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HSI2006'
        type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp
        end_time = None
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retMsg') == 'query condition error')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(sub_trade_tick_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryTradeTickMsgReqApi_022(self):
        """逐笔成交查询: BY_VOL,vol=100, direct=None isSubTrade = True, frequence=2"""
        frequence = 2
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HSI2006'
        type = QueryKLineMsgType.BY_VOL
        direct = None
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp
        end_time = None
        vol = 100
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retMsg') == 'query TradeTick msg error. unKnown QueryTradeTickDirectType')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(sub_trade_tick_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryTradeTickMsgReqApi_023(self):
        """逐笔成交查询: BY_VOL,vol=100, direct=UNKNOWN_QUERY_DIRECT, isSubTrade = True, frequence=2"""
        frequence = 2
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HSI2006'
        type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp
        end_time = None
        vol = 100
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retMsg') == 'query TradeTick msg error. unKnown QueryTradeTickDirectType')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(sub_trade_tick_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryTradeTickMsgReqApi_024(self):
        """逐笔成交查询: type = UNKNOWN_QUERY_KLINE"""
        frequence = 2
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HSI2006'
        type = QueryKLineMsgType.UNKNOWN_QUERY_KLINE
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp
        end_time = start_time_stamp
        vol = 100
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retMsg') == 'query condition error')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(sub_trade_tick_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryTradeTickMsgReqApi_025(self):
        """逐笔成交查询: isSubTrade = None时则不订阅"""
        frequence = 2
        isSubTrade = None
        exchange = 'HKFE'
        code = 'HSI2006'
        type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp
        end_time = start_time_stamp
        vol = 100
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol,
                                                    start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(sub_trade_tick_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

# --------------------------------------------------订阅逐笔成交数据-------------------------------------------------------
    def test_SubscribeTradeTickReqApi_001(self):
        """订阅一个合约的逐笔: frequence=None"""
        frequence = None
        exchange = 'HKFE'
        code = 'HSI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeTradeTickReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_SubscribeTradeTickReqApi_002(self):
        """订阅一个合约的逐笔: frequence=4"""
        frequence = 4
        exchange = 'HKFE'
        code = 'HSI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeTradeTickReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_SubscribeTradeTickReqApi_003(self):
        """订阅2个合约的逐笔: frequence=100"""
        frequence = 100
        exchange = 'HKFE'
        code1 = 'HSI2006'
        code2 = 'HHI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeTradeTickReqApi(exchange, code1, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code1)

        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeTradeTickReqApi(exchange, code2, start_time_stamp, recv_num=50))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code2)
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        recv_code_list = []
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            recv_code_list.append(self.common.searchDicKV(info, 'instrCode'))
        self.assertTrue(set(recv_code_list) == {code1, code2})

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)
        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_SubscribeTradeTickReqApi_004(self):
        """订阅一个合约的逐笔: frequence=100, exchange=UNKNOWN"""
        frequence = 100
        exchange = 'UNKNOWN'
        code = 'HSI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeTradeTickReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retMsg') == 'exchange type error')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_SubscribeTradeTickReqApi_005(self):
        """订阅一个合约的逐笔: frequence=100, code=xxxx"""
        frequence = 100
        exchange = 'HKFE'
        code = 'xxxx'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeTradeTickReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retMsg') == 'instr code [{}] error'.format(code))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

# --------------------------------------------------取消订阅逐笔成交数据-------------------------------------------------------
    def test_UnsubscribeTradeTickReqApi_001(self):
        """取消订阅一个合约的逐笔"""
        frequence = 100
        exchange = 'HKFE'
        code = 'HSI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeTradeTickReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)

        self.logger.debug(u'取消订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeTradeTickReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)

        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnsubscribeTradeTickReqApi_002(self):
        """订阅两个合约的逐笔，再取消其中一个的合约的逐笔"""
        frequence = 100
        exchange = 'HKFE'
        code1 = 'HSI2006'
        code2 = 'HHI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeTradeTickReqApi(exchange, code1, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code1)
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeTradeTickReqApi(exchange, code2, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code2)

        self.logger.debug(u'取消订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeTradeTickReqApi(exchange, code1, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code1)

        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code2)

    def test_UnsubscribeTradeTickReqApi_003(self):
        """订阅两个合约的逐笔，再取消2个的合约的逐笔"""
        frequence = 100
        exchange = 'HKFE'
        code1 = 'HSI2006'
        code2 = 'HHI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeTradeTickReqApi(exchange, code1, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code1)
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeTradeTickReqApi(exchange, code2, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code2)

        self.logger.debug(u'取消订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeTradeTickReqApi(exchange, code1, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code1)

        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeTradeTickReqApi(exchange, code2, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code2)

        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnsubscribeTradeTickReqApi_004(self):
        """通过逐笔成交查询一个合约且订阅其逐笔，通过取消逐笔订阅取消,取消成功"""
        frequence = 100
        isSubTrade = True
        exchange = 'HKFE'
        code = 'HHI2006'
        type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start_time = start_time_stamp - 5 * 60 * 1000
        end_time = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'逐笔成交查询，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryTradeTickMsgReqApi(isSubTrade, exchange, code, type, direct, start_time, end_time, vol, start_time_stamp))
        query_trade_tick_rsp_list = final_rsp['query_trade_tick_rsp_list']
        sub_trade_tick_rsp_list = final_rsp['sub_trade_tick_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_trade_tick_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_trade_tick_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=50))
        self.assertTrue(info_list.__len__() > 0)

        start_time_stamp = int(time.time() * 1000)
        self.logger.debug(u'取消订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeTradeTickReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)

        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)


    def test_UnsubscribeTradeTickReqApi_005(self):
        """订阅合约A的逐笔数据，取消订阅合约B的逐笔数据，取消失败"""
        frequence = 100
        exchange = 'HKFE'
        code = 'HSI2006'
        code2 = 'HSI2007'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeTradeTickReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)

        self.logger.debug(u'取消订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeTradeTickReqApi(exchange, code2, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retMsg') == 'instr [{}_{}] have no subscribe'.format(exchange, code2))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code2)

        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    def test_UnsubscribeTradeTickReqApi_006(self):
        """订阅合约A的逐笔数据，取消订阅不存在的合约B的逐笔数据，取消失败"""
        frequence = 100
        exchange = 'HKFE'
        code = 'HSI2006'
        code2 = 'xxxx'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeTradeTickReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)

        self.logger.debug(u'取消订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeTradeTickReqApi(exchange, code2, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code2))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code2)

        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

    def test_UnsubscribeTradeTickReqApi_007(self):
        """订阅合约A的逐笔数据，取消订阅 exchange传入UNKNOWN"""
        frequence = 100
        exchange = 'HKFE'
        exchange2 = 'UNKNOWN'
        code = 'HSI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeTradeTickReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)

        self.logger.debug(u'取消订阅逐笔数据，并检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeTradeTickReqApi(exchange2, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retMsg') == 'exchange type error')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)

        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_04_QuoteTradeData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        self.assertTrue(self.common.checkFrequence(info_list, frequence))
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)

# --------------------------------------------------查询当日分时数据-------------------------------------------------------
    def test_QueryKLineMinMsgReqApi_001(self):
        """分时查询： isSubKLineMin = True"""
        frequence = 100
        isSubKLineMin = True
        exchange = 'HKFE'
        code = 'HHI2006'
        query_type = QueryKLineMsgType.UNKNOWN_QUERY_KLINE  # app 订阅服务该字段无意义
        direct = QueryKLineDirectType.WITH_BACK  # app 订阅服务该字段无意义
        start = 0  # app 订阅服务该字段无意义
        end = 0  # app 订阅服务该字段无意义
        vol = 0  # app 订阅服务该字段无意义
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时数据查询，检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMinMsgReqApi(isSubKLineMin, exchange, code, query_type, direct, start, end, vol,
                                                    start_time_stamp))
        query_kline_min_rsp_list = final_rsp['query_kline_min_rsp_list']
        sub_kline_min_rsp_list = final_rsp['sub_kline_min_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'code') == code)

        self.assertTrue(int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'检查查询返回的当日分时数据')
        info_list = self.common.searchDicKV(query_kline_min_rsp_list[0], 'data')
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', info_list, is_before_data=True, start_sub_time=start_time_stamp, start_time=0, exchange=exchange, instr_code=code)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=10))
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)

    def test_QueryKLineMinMsgReqApi_002(self):
        """分时查询： isSubKLineMin = False"""
        frequence = 100
        isSubKLineMin = False
        exchange = 'HKFE'
        code = 'HHI2006'
        query_type = QueryKLineMsgType.UNKNOWN_QUERY_KLINE  # app 订阅服务该字段无意义
        direct = QueryKLineDirectType.WITH_BACK  # app 订阅服务该字段无意义
        start = 0  # app 订阅服务该字段无意义
        end = 0  # app 订阅服务该字段无意义
        vol = 0  # app 订阅服务该字段无意义
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时数据查询，检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMinMsgReqApi(isSubKLineMin, exchange, code, query_type, direct, start, end, vol,
                                                    start_time_stamp))
        query_kline_min_rsp_list = final_rsp['query_kline_min_rsp_list']
        sub_kline_min_rsp_list = final_rsp['sub_kline_min_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'code') == code)

        self.assertTrue(int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'检查查询返回的当日分时数据')
        info_list = self.common.searchDicKV(query_kline_min_rsp_list[0], 'data')
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', info_list, is_before_data=True, start_sub_time=start_time_stamp, start_time=0, exchange=exchange, instr_code=code)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryKLineMinMsgReqApi_003(self):
        """分时查询： isSubKLineMin = True, 订阅两个合约"""
        frequence = 100
        isSubKLineMin = True
        exchange = 'HKFE'
        code1 = 'HHI2006'
        code2 = 'HHI2006'
        query_type = QueryKLineMsgType.UNKNOWN_QUERY_KLINE  # app 订阅服务该字段无意义
        direct = QueryKLineDirectType.WITH_BACK  # app 订阅服务该字段无意义
        start = 0  # app 订阅服务该字段无意义
        end = 0  # app 订阅服务该字段无意义
        vol = 0  # app 订阅服务该字段无意义
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时数据查询，检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMinMsgReqApi(isSubKLineMin, exchange, code1, query_type, direct, start, end, vol,
                                                    start_time_stamp))
        query_kline_min_rsp_list = final_rsp['query_kline_min_rsp_list']
        sub_kline_min_rsp_list = final_rsp['sub_kline_min_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'code') == code1)
        self.assertTrue(int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'code') == code1)

        self.assertTrue(int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'检查查询返回的当日分时数据')
        info_list = self.common.searchDicKV(query_kline_min_rsp_list[0], 'data')
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', info_list, is_before_data=True, start_sub_time=start_time_stamp, start_time=0, exchange=exchange, instr_code=code1)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'查询第二个合约')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMinMsgReqApi(isSubKLineMin, exchange, code2, query_type, direct, start, end, vol,
                                                    start_time_stamp))
        query_kline_min_rsp_list = final_rsp['query_kline_min_rsp_list']
        sub_kline_min_rsp_list = final_rsp['sub_kline_min_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'code') == code2)
        self.assertTrue(int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'code') == code2)

        self.assertTrue(int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'检查查询返回的当日分时数据')
        info_list = self.common.searchDicKV(query_kline_min_rsp_list[0], 'data')
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', info_list, is_before_data=True, start_sub_time=start_time_stamp, start_time=0, exchange=exchange, instr_code=code1)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=50))
        recv_code_list = []
        for info in info_list:
            recv_code_list.append(self.common.searchDicKV(info, 'instrCode'))
        self.assertTrue(set(recv_code_list) == {code1, code2})

    def test_QueryKLineMinMsgReqApi_004(self):
        """分时查询： isSubKLineMin = True, exchange = UNKNOWN"""
        frequence = 100
        isSubKLineMin = True
        exchange = 'UNKNOWN'
        code = 'HHI2006'
        query_type = QueryKLineMsgType.UNKNOWN_QUERY_KLINE  # app 订阅服务该字段无意义
        direct = QueryKLineDirectType.WITH_BACK  # app 订阅服务该字段无意义
        start = 0  # app 订阅服务该字段无意义
        end = 0  # app 订阅服务该字段无意义
        vol = 0  # app 订阅服务该字段无意义
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时数据查询，检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMinMsgReqApi(isSubKLineMin, exchange, code, query_type, direct, start, end, vol,
                                                    start_time_stamp))
        query_kline_min_rsp_list = final_rsp['query_kline_min_rsp_list']
        sub_kline_min_rsp_list = final_rsp['sub_kline_min_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code))
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'startTimeStamp')))
        self.assertTrue(sub_kline_min_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryKLineMinMsgReqApi_005(self):
        """分时查询： isSubKLineMin = True, code = xxx"""
        frequence = 100
        isSubKLineMin = True
        exchange = 'HKFE'
        code = 'xxx'
        query_type = QueryKLineMsgType.UNKNOWN_QUERY_KLINE  # app 订阅服务该字段无意义
        direct = QueryKLineDirectType.WITH_BACK  # app 订阅服务该字段无意义
        start = 0  # app 订阅服务该字段无意义
        end = 0  # app 订阅服务该字段无意义
        vol = 0  # app 订阅服务该字段无意义
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时数据查询，检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMinMsgReqApi(isSubKLineMin, exchange, code, query_type, direct, start, end, vol,
                                                    start_time_stamp))
        query_kline_min_rsp_list = final_rsp['query_kline_min_rsp_list']
        sub_kline_min_rsp_list = final_rsp['sub_kline_min_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code))
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'code') == code)
        self.assertTrue(int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'startTimeStamp')))
        self.assertTrue(sub_kline_min_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryKLineMinMsgReqApi_006(self):
        """分时查询： isSubKLineMin = True, code = None"""
        frequence = 100
        isSubKLineMin = True
        exchange = 'HKFE'
        code = None
        query_type = QueryKLineMsgType.UNKNOWN_QUERY_KLINE  # app 订阅服务该字段无意义
        direct = QueryKLineDirectType.WITH_BACK  # app 订阅服务该字段无意义
        start = 0  # app 订阅服务该字段无意义
        end = 0  # app 订阅服务该字段无意义
        vol = 0  # app 订阅服务该字段无意义
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时数据查询，检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMinMsgReqApi(isSubKLineMin, exchange, code, query_type, direct, start, end, vol,
                                                    start_time_stamp))
        query_kline_min_rsp_list = final_rsp['query_kline_min_rsp_list']
        sub_kline_min_rsp_list = final_rsp['sub_kline_min_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'retMsg') == 'instr [ {} ] error'.format(exchange))
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(query_kline_min_rsp_list[0], 'startTimeStamp')))
        self.assertTrue(sub_kline_min_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

# --------------------------------------------------查询五日分时数据-------------------------------------------------------
    def test_QueryFiveDaysKLineMinReqApi_001(self):
        """分时查询： isSubKLineMin = True"""
        frequence = 100
        isSubKLineMin = True
        exchange = 'HKFE'
        code = 'HHI2006'
        start = None    # app 订阅服务该字段无意义
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'五日分时数据查询，检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryFiveDaysKLineMinReqApi(isSubKLineMin, exchange, code, start, start_time_stamp))
        query_5day_klinemin_rsp_list = final_rsp['query_5day_klinemin_rsp_list']
        sub_kline_min_rsp_list = final_rsp['sub_kline_min_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'code') == code)
        self.assertTrue(
            int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'code') == code)

        self.assertTrue(
            int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'startTimeStamp')))
        self.logger.debug(u'检查查询返回的五日分时数据')
        info_list = self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'data')
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', info_list, is_before_data=True,
                                                     start_sub_time=start_time_stamp, start_time=0,
                                                     exchange=exchange, instr_code=code)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=10))
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)

    def test_QueryFiveDaysKLineMinReqApi_002(self):
        """分时查询： isSubKLineMin = False"""
        frequence = 100
        isSubKLineMin = False
        exchange = 'HKFE'
        code = 'HHI2006'
        start = None    # app 订阅服务该字段无意义
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'五日分时数据查询，检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryFiveDaysKLineMinReqApi(isSubKLineMin, exchange, code, start, start_time_stamp))
        query_5day_klinemin_rsp_list = final_rsp['query_5day_klinemin_rsp_list']
        sub_kline_min_rsp_list = final_rsp['sub_kline_min_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'code') == code)
        self.assertTrue(
            int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(sub_kline_min_rsp_list.__len__() == 0)

        self.logger.debug(u'检查查询返回的五日分时数据')
        info_list = self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'data')
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', info_list, is_before_data=True,
                                                     start_sub_time=start_time_stamp, start_time=0,
                                                     exchange=exchange, instr_code=code)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryFiveDaysKLineMinReqApi_003(self):
        """分时查询： isSubKLineMin = None"""
        frequence = 100
        isSubKLineMin = None
        exchange = 'HKFE'
        code = 'HHI2006'
        start = None    # app 订阅服务该字段无意义
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'五日分时数据查询，检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryFiveDaysKLineMinReqApi(isSubKLineMin, exchange, code, start, start_time_stamp))
        query_5day_klinemin_rsp_list = final_rsp['query_5day_klinemin_rsp_list']
        sub_kline_min_rsp_list = final_rsp['sub_kline_min_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'code') == code)
        self.assertTrue(
            int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'startTimeStamp')))
        self.assertTrue(sub_kline_min_rsp_list.__len__() == 0)
        self.logger.debug(u'检查查询返回的五日分时数据')
        info_list = self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'data')
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', info_list, is_before_data=True,
                                                     start_sub_time=start_time_stamp, start_time=0,
                                                     exchange=exchange, instr_code=code)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryFiveDaysKLineMinReqApi_004(self):
        """分时查询： exchange = UNKNOWN"""
        frequence = 100
        isSubKLineMin = True
        exchange = 'UNKNOWN'
        code = 'HHI2006'
        start = None    # app 订阅服务该字段无意义
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'五日分时数据查询，检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryFiveDaysKLineMinReqApi(isSubKLineMin, exchange, code, start, start_time_stamp))
        query_5day_klinemin_rsp_list = final_rsp['query_5day_klinemin_rsp_list']
        sub_kline_min_rsp_list = final_rsp['sub_kline_min_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code))
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'code') == code)
        self.assertTrue(
            int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(sub_kline_min_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryFiveDaysKLineMinReqApi_005(self):
        """分时查询： code = xxxx"""
        frequence = 100
        isSubKLineMin = True
        exchange = 'HKFE'
        code = 'xxxx'
        start = None    # app 订阅服务该字段无意义
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'五日分时数据查询，检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryFiveDaysKLineMinReqApi(isSubKLineMin, exchange, code, start, start_time_stamp))
        query_5day_klinemin_rsp_list = final_rsp['query_5day_klinemin_rsp_list']
        sub_kline_min_rsp_list = final_rsp['sub_kline_min_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code))
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'code') == code)
        self.assertTrue(
            int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(sub_kline_min_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryFiveDaysKLineMinReqApi_006(self):
        """分时查询： code = UBmain"""
        frequence = 100
        isSubKLineMin = True
        exchange = 'HKFE'
        code = 'UBmain'
        start = None    # app 订阅服务该字段无意义
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'五日分时数据查询，检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryFiveDaysKLineMinReqApi(isSubKLineMin, exchange, code, start, start_time_stamp))
        query_5day_klinemin_rsp_list = final_rsp['query_5day_klinemin_rsp_list']
        sub_kline_min_rsp_list = final_rsp['sub_kline_min_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code))
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'code') == code)
        self.assertTrue(
            int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'startTimeStamp')))

        self.assertTrue(sub_kline_min_rsp_list.__len__() == 0)
        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() == 0)

# --------------------------------------------------订阅分时数据-------------------------------------------------------
    def test_SubscribeKlineMinReqApi_001(self):
        """分时订阅一个合约"""
        frequence = 100
        exchange = 'HKFE'
        code = 'HHI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时订阅，检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeKlineMinReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)
        self.assertTrue(
            int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=20))
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)

    def test_SubscribeKlineMinReqApi_002(self):
        """分时订阅2个合约"""
        frequence = 100
        exchange = 'HKFE'
        code1 = 'HSI2006'
        code2 = 'HHI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时订阅，检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeKlineMinReqApi(exchange, code1, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code1)
        self.assertTrue(
            int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'分时订阅，检查返回结果2')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeKlineMinReqApi(exchange, code2, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code2)
        self.assertTrue(
            int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_06_PushKLineMinData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        recv_code_list = []
        for info in info_list:
            recv_code_list.append(self.common.searchDicKV(info, 'code'))
        self.assertTrue(set(recv_code_list) == {code1, code2})

    def test_SubscribeKlineMinReqApi_003(self):
        """分时订阅一个合约, code=xxxx"""
        frequence = 100
        exchange = 'HKFE'
        code = 'xxxx'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时订阅，检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeKlineMinReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(
            int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() == 0)

    def test_SubscribeKlineMinReqApi_004(self):
        """分时订阅一个合约, exchange='UNKNOWN'"""
        frequence = 100
        exchange = 'UNKNOWN'
        code = 'HHI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时订阅，检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeKlineMinReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)
        self.assertTrue(
            int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() == 0)

    def test_SubscribeKlineMinReqApi_005(self):
        """分时订阅一个合约, code=TNmain"""
        frequence = 100
        exchange = 'HKFE'
        code = 'TNmain'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时订阅，检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeKlineMinReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(
            int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() == 0)

# --------------------------------------------------取消订阅分时数据-------------------------------------------------------
    def test_UnsubscribeKlineMinReqApi_001(self):
        """分时订阅一个合约,取消订阅"""
        frequence = 100
        exchange = 'HKFE'
        code = 'HHI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时订阅，检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeKlineMinReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() > 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)

        self.logger.debug(u'取消订阅,并校验')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeKlineMinReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)
        self.assertTrue(
            int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnsubscribeKlineMinReqApi_002(self):
        """分时订阅2个合约,取消订阅其中一个"""
        frequence = 100
        exchange = 'HKFE'
        code1 = 'HHI2006'
        code2 = 'HSI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时订阅，检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeKlineMinReqApi(exchange, code1, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.logger.debug(u'分时订阅，检查返回结果2')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeKlineMinReqApi(exchange, code2, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'取消订阅,并校验')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeKlineMinReqApi(exchange, code1, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code1)
        self.assertTrue(
            int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() > 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'code') == code2)

    def test_UnsubscribeKlineMinReqApi_003(self):
        """分时订阅2个合约,取消订阅2个"""
        frequence = 100
        exchange = 'HKFE'
        code1 = 'HHI2006'
        code2 = 'HSI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时订阅，检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeKlineMinReqApi(exchange, code1, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.logger.debug(u'分时订阅，检查返回结果2')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeKlineMinReqApi(exchange, code2, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'取消订阅,并校验')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeKlineMinReqApi(exchange, code1, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code1)
        self.assertTrue(
            int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'取消订阅,并校验2')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeKlineMinReqApi(exchange, code2, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code2)
        self.assertTrue(
            int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnsubscribeKlineMinReqApi_004(self):
        """查询分时时顺便订阅了分时，再取消分时订阅"""
        frequence = 100
        isSubKLineMin = True
        exchange = 'HKFE'
        code = 'HHI2006'
        query_type = QueryKLineMsgType.UNKNOWN_QUERY_KLINE  # app 订阅服务该字段无意义
        direct = QueryKLineDirectType.WITH_BACK  # app 订阅服务该字段无意义
        start = 0  # app 订阅服务该字段无意义
        end = 0  # app 订阅服务该字段无意义
        vol = 0  # app 订阅服务该字段无意义
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时数据查询，检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMinMsgReqApi(isSubKLineMin, exchange, code, query_type, direct, start, end, vol,
                                                   start_time_stamp))
        query_kline_min_rsp_list = final_rsp['query_kline_min_rsp_list']
        sub_kline_min_rsp_list = final_rsp['sub_kline_min_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_min_rsp_list[0], 'retCode') == 'SUCCESS')

        self.assertTrue(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() > 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)

        self.logger.debug(u'取消订阅,并校验')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeKlineMinReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)
        self.assertTrue(
            int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() == 0)

    def test_UnsubscribeKlineMinReqApi_005(self):
        """查询5日分时时顺便订阅了分时，再取消分时订阅"""
        frequence = 100
        isSubKLineMin = True
        exchange = 'HKFE'
        code = 'HHI2006'
        start = None  # app 订阅服务该字段无意义
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'五日分时数据查询，检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryFiveDaysKLineMinReqApi(isSubKLineMin, exchange, code, start, start_time_stamp))
        query_5day_klinemin_rsp_list = final_rsp['query_5day_klinemin_rsp_list']
        sub_kline_min_rsp_list = final_rsp['sub_kline_min_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_5day_klinemin_rsp_list[0], 'retCode') == 'SUCCESS')

        self.assertTrue(self.common.searchDicKV(sub_kline_min_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=10))
        self.assertTrue(info_list.__len__() > 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == 'HKFE')
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)

        self.logger.debug(u'取消订阅,并校验')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeKlineMinReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)
        self.assertTrue(
            int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() == 0)


    def test_UnsubscribeKlineMinReqApi_006(self):
        """分时订阅一个合约,取消订阅一个未订阅的合约"""
        frequence = 100
        exchange = 'HKFE'
        code = 'HHI2006'
        code2 = 'HSI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时订阅，检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeKlineMinReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'取消订阅,并校验')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeKlineMinReqApi(exchange, code2, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retMsg') == 'instr have no subscribe')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code2)
        self.assertTrue(
            int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() > 0)

    def test_UnsubscribeKlineMinReqApi_007(self):
        """分时订阅一个合约,取消订阅入参exchange=UNKNOWN"""
        frequence = 100
        exchange = 'HKFE'
        exchange2 = 'UNKNOWN'
        code = 'HHI2006'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时订阅，检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeKlineMinReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'取消订阅,并校验')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeKlineMinReqApi(exchange2, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retMsg') == 'instr [ {}_{} ] error'.format(exchange2, code))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code)
        self.assertTrue(
            int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() > 0)

    def test_UnsubscribeKlineMinReqApi_008(self):
        """分时订阅一个合约,取消订阅一个不存在的合约"""
        frequence = 100
        exchange = 'HKFE'
        code = 'HHI2006'
        code2 = 'xxxx'
        start_time_stamp = int(time.time() * 1000)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'分时订阅，检查返回结果')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.SubscribeKlineMinReqApi(exchange, code, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'取消订阅,并校验')
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnsubscribeKlineMinReqApi(exchange, code2, start_time_stamp))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'retMsg') == 'instr [ {}_{} ] error'.format(exchange, code2))
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(rsp_list[0], 'code') == code2)
        self.assertTrue(
            int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(rsp_list[0], 'startTimeStamp')))

        self.logger.debug(u'通过接收分时数据的接口，筛选出分时数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineMinDataApi(recv_num=20))
        self.assertTrue(info_list.__len__() > 0)

# --------------------------------------------------查询历史K线-------------------------------------------------------
    def test_QueryKLineMsgReqApi_001(self):
        """K线查询: BY_DATE_TIME, 1分K, 前5分钟的数据, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'HHI2006'
        peroid_type = KLinePeriodType.MINUTE
        query_type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.UNKNOWN_QUERY_DIRECT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 5 * 60 * 1000
        end = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end, vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, is_before_data=True, start_sub_time=end, start_time=start, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=10))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'MINUTE')

    def test_QueryKLineMsgReqApi_002(self):
        """K线查询: BY_DATE_TIME, 3分K, 前30分钟的数据, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'HSI2006'
        peroid_type = KLinePeriodType.THREE_MIN
        query_type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.UNKNOWN_QUERY_DIRECT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 30 * 60 * 1000
        end = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end, vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=end, is_before_data=True, start_time=start, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'THREE_MIN')

    def test_QueryKLineMsgReqApi_003(self):
        """K线查询: BY_DATE_TIME, 5分K, 前40分钟的数据, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'HSI2006'
        peroid_type = KLinePeriodType.FIVE_MIN
        query_type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.UNKNOWN_QUERY_DIRECT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 40 * 60 * 1000
        end = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end, vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=end, is_before_data=True, start_time=start, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'FIVE_MIN')

    def test_QueryKLineMsgReqApi_004(self):
        """K线查询: BY_DATE_TIME, 15分K, 前45分钟的数据, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'HSI2006'
        peroid_type = KLinePeriodType.FIFTEEN_MIN
        query_type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.UNKNOWN_QUERY_DIRECT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 45 * 60 * 1000
        end = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end, vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=end, is_before_data=True, start_time=start, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'FIFTEEN_MIN')

    def test_QueryKLineMsgReqApi_005(self):
        """K线查询: BY_DATE_TIME, 30分K, 前4小时的数据, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.THIRTY_MIN
        query_type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.UNKNOWN_QUERY_DIRECT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 4 * 60 * 60 * 1000
        end = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end, vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=end, is_before_data=True, start_time=start, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'THIRTY_MIN')

    def test_QueryKLineMsgReqApi_006(self):
        """K线查询: BY_DATE_TIME, 60分K, 前4小时的数据, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.HOUR
        query_type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.UNKNOWN_QUERY_DIRECT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 4 * 60 * 60 * 1000
        end = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end, vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=end, is_before_data=True, start_time=start, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'HOUR')

    def test_QueryKLineMsgReqApi_007(self):
        """K线查询: BY_DATE_TIME, 120分K, 前4小时的数据, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.TWO_HOUR
        query_type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.UNKNOWN_QUERY_DIRECT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 4 * 60 * 60 * 1000
        end = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end, vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=end, is_before_data=True, start_time=start, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'TWO_HOUR')

    def test_QueryKLineMsgReqApi_008(self):
        """K线查询: BY_DATE_TIME, 240分K, 前1天的数据, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.FOUR_HOUR
        query_type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.UNKNOWN_QUERY_DIRECT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 24 * 60 * 60 * 1000
        end = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end, vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=end, is_before_data=True, start_time=start, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'FOUR_HOUR')

    def test_QueryKLineMsgReqApi_009(self):
        """K线查询: BY_DATE_TIME, 日K, 前2天的数据, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.DAY
        query_type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.UNKNOWN_QUERY_DIRECT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 48 * 60 * 60 * 1000
        end = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end, vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=end, is_before_data=True, start_time=start, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'DAY')

    def test_QueryKLineMsgReqApi_010(self):
        """K线查询: BY_DATE_TIME, 周K, 前2周的数据, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.WEEK
        query_type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.UNKNOWN_QUERY_DIRECT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 2 * 5 * 48 * 60 * 60 * 1000
        end = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end, vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=end, is_before_data=True, start_time=start, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'WEEK')

    def test_QueryKLineMsgReqApi_011(self):
        """K线查询: BY_DATE_TIME, 月K, 前一个月的数据, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.MONTH
        query_type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.UNKNOWN_QUERY_DIRECT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 4 * 5 * 48 * 60 * 60 * 1000
        end = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end, vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=end, is_before_data=True, start_time=start, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'MONTH')

    def test_QueryKLineMsgReqApi_012(self):
        """K线查询: BY_DATE_TIME, 1分K, 前5分钟的数据, isSubKLine = False, frequence=2"""
        frequence = 100
        isSubKLine = False
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.MINUTE
        query_type = QueryKLineMsgType.BY_DATE_TIME
        direct = QueryKLineDirectType.UNKNOWN_QUERY_DIRECT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 5 * 60 * 1000
        end = start_time_stamp
        vol = None
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end, vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(sub_kline_rsp_list.__len__() == 0)

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=end, is_before_data=True, start_time=start, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口,此时获取不到K线数据')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

    def test_QueryKLineMsgReqApi_013(self):
        """K线查询: BY_VOL, 1分钟K，向前查询100根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MCH2006'
        peroid_type = KLinePeriodType.MINUTE
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_FRONT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp
        end = None
        vol = 100
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end, vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time= start, is_before_data=True, start_time=0, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'MINUTE')

    def test_QueryKLineMsgReqApi_014(self):
        """K线查询: BY_VOL, 3分K, 向前查询100根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'HSI2006'
        peroid_type = KLinePeriodType.THREE_MIN
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_FRONT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp
        end = None
        vol = 100
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time= start, is_before_data=True, start_time=0, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'THREE_MIN')

    def test_QueryKLineMsgReqApi_015(self):
        """K线查询: BY_VOL, 5分K, 向前查询10根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'HSI2006'
        peroid_type = KLinePeriodType.FIVE_MIN
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_FRONT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp
        end = None
        vol = 10
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time= start, is_before_data=True, start_time=0, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'FIVE_MIN')

    def test_QueryKLineMsgReqApi_016(self):
        """K线查询: BY_VOL, 15分K, 向前获取10根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'HSI2006'
        peroid_type = KLinePeriodType.FIFTEEN_MIN
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_FRONT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp
        end = None
        vol = 10
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time= start, is_before_data=True, start_time=0, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'FIFTEEN_MIN')

    def test_QueryKLineMsgReqApi_017(self):
        """K线查询: BY_DATE_TIME, 30分K, 向前查询10根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.THIRTY_MIN
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_FRONT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp
        end = None
        vol = 10
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time= start, is_before_data=True, start_time=0, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'THIRTY_MIN')

    def test_QueryKLineMsgReqApi_018(self):
        """K线查询: BY_VOL, 60分K, 向前获取4根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.HOUR
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_FRONT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp
        end = None
        vol = 4
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=start,
                                                     is_before_data=True, start_time=0, exchange=exchange,
                                                     instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'HOUR')

    def test_QueryKLineMsgReqApi_019(self):
        """K线查询: BY_VOL, 120分K, 向前获取5根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.TWO_HOUR
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_FRONT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 3 * 24 * 60 * 60 * 1000
        end = None
        vol = 5
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time= start, is_before_data=True, start_time=0, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'TWO_HOUR')

    def test_QueryKLineMsgReqApi_020(self):
        """K线查询: BY_VOL, 240分K, 向前获取3根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.FOUR_HOUR
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_FRONT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp
        end = None
        vol = 3
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time= start, is_before_data=True, start_time=0, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'FOUR_HOUR')

    def test_QueryKLineMsgReqApi_021(self):
        """K线查询: BY_VOL, 日K, 向前获取5根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.DAY
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_FRONT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp
        end = None
        vol = 5
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time= start, is_before_data=True, start_time=0, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'DAY')

    def test_QueryKLineMsgReqApi_022(self):
        """K线查询: BY_VOL, 周K, 向前获取2根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.WEEK
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_FRONT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp
        end = None
        vol = 2
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time= start, is_before_data=True, start_time=0, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'WEEK')

    def test_QueryKLineMsgReqApi_023(self):
        """K线查询: BY_VOL, 月K, 向前获取1根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.MONTH
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_FRONT
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp
        end = None
        vol = 1
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time= start, is_before_data=True, start_time=0, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'MONTH')


    def test_QueryKLineMsgReqApi_024(self):
        """K线查询: BY_VOL, 1分钟K，向后查询50根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MCH2006'
        peroid_type = KLinePeriodType.MINUTE
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 3 * 24 * 60 * 60 * 1000
        end = None
        vol = 50
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end, vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=start_time_stamp, is_before_data=True, start_time=start, exchange=exchange, instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'MINUTE')

    def test_QueryKLineMsgReqApi_025(self):
        """K线查询: BY_VOL, 3分K, 向后查询100根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'HSI2006'
        peroid_type = KLinePeriodType.THREE_MIN
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 3 * 24 * 60 * 60 * 1000
        end = None
        vol = 100
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=start_time_stamp,
                                                     is_before_data=True, start_time=start, exchange=exchange,
                                                     instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'THREE_MIN')

    def test_QueryKLineMsgReqApi_026(self):
        """K线查询: BY_VOL, 5分K, 向后查询10根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'HSI2006'
        peroid_type = KLinePeriodType.FIVE_MIN
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 3 * 24 * 60 * 60 * 1000
        end = None
        vol = 10
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=start_time_stamp,
                                                     is_before_data=True, start_time=start, exchange=exchange,
                                                     instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'FIVE_MIN')

    def test_QueryKLineMsgReqApi_027(self):
        """K线查询: BY_VOL, 15分K, 向后获取10根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'HSI2006'
        peroid_type = KLinePeriodType.FIFTEEN_MIN
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 3 * 24 * 60 * 60 * 1000
        end = None
        vol = 10
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=start_time_stamp,
                                                     is_before_data=True, start_time=start, exchange=exchange,
                                                     instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'FIFTEEN_MIN')

    def test_QueryKLineMsgReqApi_028(self):
        """K线查询: BY_DATE_TIME, 30分K, 向后查询10根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.THIRTY_MIN
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 3 * 24 * 60 * 60 * 1000
        end = None
        vol = 10
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=start_time_stamp,
                                                     is_before_data=True, start_time=start, exchange=exchange,
                                                     instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'THIRTY_MIN')

    def test_QueryKLineMsgReqApi_029(self):
        """K线查询: BY_VOL, 60分K, 向后获取5根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.HOUR
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 3 * 24 * 60 * 60 * 1000
        end = None
        vol = 5
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=start_time_stamp,
                                                     is_before_data=True, start_time=start, exchange=exchange,
                                                     instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'HOUR')

    def test_QueryKLineMsgReqApi_030(self):
        """K线查询: BY_VOL, 120分K, 向后获取5根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.TWO_HOUR
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 3 * 24 * 60 * 60 * 1000
        end = None
        vol = 5
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=start_time_stamp,
                                                     is_before_data=True, start_time=start, exchange=exchange,
                                                     instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'TWO_HOUR')

    def test_QueryKLineMsgReqApi_031(self):
        """K线查询: BY_VOL, 240分K, 向后获取3根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.FOUR_HOUR
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 3 * 24 * 60 * 60 * 1000
        end = None
        vol = 3
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=start_time_stamp,
                                                     is_before_data=True, start_time=start, exchange=exchange,
                                                     instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'FOUR_HOUR')

    def test_QueryKLineMsgReqApi_032(self):
        """K线查询: BY_VOL, 日K, 向后获取5根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.DAY
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 3 * 24 * 60 * 60 * 1000
        end = None
        vol = 5
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=start_time_stamp,
                                                     is_before_data=True, start_time=start, exchange=exchange,
                                                     instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'DAY')

    def test_QueryKLineMsgReqApi_033(self):
        """K线查询: BY_DATE_TIME, 周K, 向后获取2根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.WEEK
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 3 * 24 * 60 * 60 * 1000
        end = None
        vol = 2
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=start_time_stamp,
                                                     is_before_data=True, start_time=start, exchange=exchange,
                                                     instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'WEEK')

    def test_QueryKLineMsgReqApi_034(self):
        """K线查询: BY_DATE_TIME, 月K, 向后获取1根K线, isSubKLine = True, frequence=2"""
        frequence = 100
        isSubKLine = True
        exchange = 'HKFE'
        code = 'MHI2006'
        peroid_type = KLinePeriodType.MONTH
        query_type = QueryKLineMsgType.BY_VOL
        direct = QueryKLineDirectType.WITH_BACK
        start_time_stamp = int(time.time() * 1000)
        start = start_time_stamp - 3 * 24 * 60 * 60 * 1000
        end = None
        vol = 1
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp, frequence=frequence))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        self.logger.debug(u'查询K线数据，并检查返回结果')
        final_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.QueryKLineMsgReqApi(isSubKLine, exchange, code, peroid_type, query_type, direct, start, end,
                                                vol, start_time_stamp))
        query_kline_rsp_list = final_rsp['query_kline_rsp_list']
        sub_kline_rsp_list = final_rsp['sub_kline_rsp_list']
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'retMsg') == 'query kline msg success')
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'exchange') == exchange)
        self.assertTrue(self.common.searchDicKV(query_kline_rsp_list[0], 'code') == code)

        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(sub_kline_rsp_list[0], 'retMsg') == 'Subscribe KLine success')

        self.logger.debug(u'校验回包里的历史k线数据')
        k_data_list = self.common.searchDicKV(query_kline_rsp_list[0], 'kData')
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', k_data_list, start_sub_time=start_time_stamp,
                                                     is_before_data=True, start_time=start, exchange=exchange,
                                                     instr_code=code, peroid_type=peroid_type)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)

        self.logger.debug(u'通过接收k线数据的接口，筛选出k线数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.PushKLineDataApi(recv_num=100))
        inner_test_result = self.inner_zmq_test_case('test_07_PushKLineData', info_list)
        self.assertTrue(inner_test_result.failures.__len__() + inner_test_result.errors.__len__() == 0)
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'exchange') == exchange)
            self.assertTrue(self.common.searchDicKV(info, 'code') == code)
            self.assertTrue(self.common.searchDicKV(info, 'peroidType') == 'MONTH')