# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/4/29
# @Software: PyCharm

import unittest
from websocket_py3.ws_api.subscribe_server_api import *
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
        self.api = SubscribeApi(delay_ws_url, self.new_loop)
        asyncio.get_event_loop().run_until_complete(future=self.api.client.ws_connect())

    def tearDown(self):
        asyncio.set_event_loop(self.new_loop)
        self.api.client.disconnect()

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
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)
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
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

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
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

    def test_LogoutReq03(self):
        """校验退出之后响应成功，且接不到订阅数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code = 'HHI2009'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.get_event_loop().run_until_complete(future=self.api.DelaySubsQutoMsgReqApi(
            sub_type=sub_type, child_type=None, base_info=base_info, start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.LogoutReq(start_time_stamp=start_time_stamp, recv_num=10))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接受时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)
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
    #
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
        time.sleep(50)
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
    #
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
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvTime')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTime')) - tolerance_time)


    # --------------------------------------按合约订阅-----------------------------------------

    def test_Instr_01(self):
        """按合约代码订阅时，订阅一个合约"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code = 'HSI2005'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
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
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 1)
        for info in before_basic_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 1)
        for info in before_snapshot_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=1000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_Instr_02(self):
        """按合约代码订阅时，订阅多个合约"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code1 = 'HSI2005'
        code2 = 'HHI2005'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
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
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 2)
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'instrCode') in [code1, code2])
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[1], 'instrCode') in [code1, code2])
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'instrCode') != self.common.searchDicKV(
            before_basic_json_list[1], 'instrCode'))
        for info in before_basic_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 2)
        self.assertTrue(self.common.searchDicKV(before_snapshot_json_list[0], 'instrCode') in [code1, code2])
        self.assertTrue(self.common.searchDicKV(before_snapshot_json_list[1], 'instrCode') in [code1, code2])
        self.assertTrue(self.common.searchDicKV(before_snapshot_json_list[0], 'instrCode') != self.common.searchDicKV(
            before_snapshot_json_list[1], 'instrCode'))
        for info in before_snapshot_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_Instr_03(self):
        """订阅一个正确的合约代码，一个错误的合约代码"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code1 = 'HSI2005'
        code2 = 'xxxx'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue(
            'instrument code [ {} ] is unknown'.format(code2) == self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 1)
        for info in before_basic_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 1)
        for info in before_snapshot_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_Instr_04(self):
        """订阅多个合约代码，其中一个为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code1 = 'HSI2005'
        code2 = 'xxxx'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue('instrument code [ {} ] is unknown'.format(code2) == self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_INSTR')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 1)
        for info in before_basic_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 1)
        for info in before_snapshot_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    # --------------------------------------------按品种订阅----------------------------------------------
    def test_Product_01(self):
        """订阅单市场，单品种"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code = 'HHI'
        base_info = [{'exchange': 'HKFE', 'product_code': product_code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))

        first_rsp_list = rsp_list['first_rsp_list']
        before_basic_json_list = rsp_list['before_basic_json_list']
        before_snapshot_json_list = rsp_list['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() > 0)
        for info in before_basic_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))     # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() > 0)
        for info in before_snapshot_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_Product_02(self):
        """
        订阅多个品种
        """
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code1 = 'HHI'
        product_code2 = 'HSI'
        base_info = [{'exchange': 'HKFE', 'product_code': product_code1},
                     {'exchange': 'HKFE', 'product_code': product_code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, base_info=base_info, start_time_stamp=start_time_stamp))

        first_rsp_list = rsp_list['first_rsp_list']
        before_basic_json_list = rsp_list['before_basic_json_list']
        before_snapshot_json_list = rsp_list['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() > 0)
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'productCode') in [product_code1, product_code2])
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[1], 'productCode') in [product_code1, product_code2])
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'productCode') != self.common.searchDicKV(
            before_basic_json_list[1], 'instrCode'))
        for info in before_basic_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() > 0)
        self.assertTrue(self.common.searchDicKV(before_snapshot_json_list[0], 'productCode') in (product_code1, product_code2))
        self.assertTrue(self.common.searchDicKV(before_snapshot_json_list[1], 'productCode') in (product_code1, product_code2))
        self.assertTrue(self.common.searchDicKV(before_snapshot_json_list[0], 'productCode') != self.common.searchDicKV(
            before_snapshot_json_list[1], 'instrCode'))
        for info in before_snapshot_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code1, product_code2))
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code1, product_code2))
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') in (product_code1, product_code2))
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_Product_03(self):
        """订阅一个正确的品种，一个错误的品种"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code1 = 'HHI'
        product_code2 = 'xxx'
        base_info = [{'exchange': 'HKFE', 'product_code': product_code1},
                     {'exchange': 'HKFE', 'product_code': product_code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))

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
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue('product code [ {} ] is unknown'.format(product_code2) ==
                        self.common.searchDicKV(first_rsp_list[1],'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') is None)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() > 0)
        for info in before_basic_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() > 0)
        for info in before_snapshot_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_Product_04(self):
        """订阅多个品种，其中一个productcode为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_PRODUCT
        product_code1 = 'HHI'
        product_code2 = None
        base_info = [{'exchange': 'HKFE', 'product_code': product_code1},
                     {'exchange': 'HKFE', 'product_code': product_code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))

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
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue('product code is null' == self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_PRODUCT')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') is None)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')))

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() > 0)
        for info in before_basic_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() > 0)
        for info in before_snapshot_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'productCode') == product_code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    # ---------------------------------------- 按市场订阅-----------------------------------------------------

    def test_Market_01(self):
        """ 按市场订阅，订阅一个市场(code不传入参数)"""
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        base_info = [{'exchange': 'HKFE'}]
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() > 0)
        for info in before_basic_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() > 0)
        for info in before_snapshot_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=5000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=3000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_Market_02(self):
        """ 按市场订阅，订阅一个市场,code不为空"""
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        base_info = [{'exchange': 'HKFE', 'code': 'HHI2005'}]

        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() > 0)
        for info in before_basic_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() > 0)
        for info in before_snapshot_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=1000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=1000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=3000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_Market_003(self):
        """ 按市场订阅，订阅多个市场"""
        sub_type = SubscribeMsgType.SUB_WITH_MARKET
        exchange1 = 'HKFE'
        exchange2 = 'SGX'
        exchange3 = 'CME'
        base_info = [{'exchange': exchange1}, {'exchange': exchange2}, {'exchange': exchange3}]
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MARKET')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') is None)
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() > 0)
        for info in before_basic_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() > 0)
        for info in before_snapshot_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=1000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=1000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=3000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    # -------------------------------------------订阅静态---------------------------------------------------

    def test_QuoteBasicInfo_Msg_001(self):
        """ 订阅单个市场、单个合约的静态数据 """
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code = 'HHI2009'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_BASIC')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 1)
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'instrCode') == code)
        for info in before_basic_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

            self.logger.debug(u'前快照数据校验')
            self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 不返回快照数据

    def test_QuoteBasicInfo_Msg_002(self):
        """ 订阅单个市场、多个合约的静态数据 """
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code1 = 'HHI2009'
        code2 = 'HHI2005'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'静态数据校验')
        self.assertTrue(before_basic_json_list.__len__() == 2)  # 应仅返回两条
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'instrCode') in [code1, code2])
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[1], 'instrCode') in [code1, code2])
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'instrCode') != self.common.searchDicKV(
            before_basic_json_list[1], 'instrCode'))
        for info in before_basic_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致
            self.logger.debug(u'前快照数据校验')
            self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 不返回快照数据

    def test_QuoteBasicInfo_Msg_003(self):
        """ 传入多个合约code，部分code错误"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code1 = 'xxxx'
        code2 = 'HHI2009'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              recv_num=2, start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue(
            self.common.searchDicKV(first_rsp_list[1], 'retMsg') == 'instrument code [ {} ] is unknown'.format(code1))

        self.logger.debug(u'静态数据校验')
        self.assertTrue(before_basic_json_list.__len__() == 1)  # 仅返回code2的静态数据
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'instrCode') == code2)
        for info in before_basic_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'前快照数据校验')
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 不返回快照数据

    # -----------------------------------------订阅快照数据----------------------------------------------------
    def test_QuoteSnapshotApi_01(self):
        """订阅单市场，单合约的快照数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code = 'HHI2005'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
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
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 1)
        for info in before_basic_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        for info in before_snapshot_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_QuoteSnapshotApi_02(self):
        """订阅单市场，多合约的快照数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2005'
        code2 = 'HSI2005'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        start_time_stamp = int(time.time() * 1000)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=1))
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
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 2)
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'instrCode') in [code1, code2])
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[1], 'instrCode') in [code1, code2])
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'instrCode') != self.common.searchDicKV(
            before_basic_json_list[1], 'instrCode'))
        for info in before_basic_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致
        self.logger.debug(u'校验前快照数据')
        self.assertTrue(self.common.searchDicKV(before_snapshot_json_list[0], 'instrCode') in [code1, code2])
        self.assertTrue(self.common.searchDicKV(before_snapshot_json_list[1], 'instrCode') in [code1, code2])
        self.assertTrue(self.common.searchDicKV(before_snapshot_json_list[0], 'instrCode') != self.common.searchDicKV(
            before_snapshot_json_list[1], 'instrCode'))
        for info in before_snapshot_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_QuoteSnapshotApi_03(self):
        """订阅单市场，多合约的快照数据，部分合约代码为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2005'
        code2 = None
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))
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
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue('instrument code is null' == self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'childType') == 'SUB_SNAPSHOT'))
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 1)
        for info in before_basic_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 1)
        for info in before_snapshot_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    # -----------------------------------------订阅盘口数据----------------------------------------------------
    def test_QuoteOrderBookDataApi_01(self):
        """订阅单市场，单合约的盘口数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code = 'HSI2005'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
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
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 1)
        for info in before_basic_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 1)
        for info in before_snapshot_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_QuoteOrderBookDataApi_02(self):
        """订阅单市场，多合约盘口数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HSI2005'
        code2 = 'HHI2005'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=1))

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
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() == 2)
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'instrCode') in [code1, code2])
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[1], 'instrCode') in [code1, code2])
        self.assertTrue(self.common.searchDicKV(before_basic_json_list[0], 'instrCode') != self.common.searchDicKV(
            before_basic_json_list[1], 'instrCode'))
        for info in before_basic_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() == 2)
        self.assertTrue(self.common.searchDicKV(before_snapshot_json_list[0], 'instrCode') in [code1, code2])
        self.assertTrue(self.common.searchDicKV(before_snapshot_json_list[1], 'instrCode') in [code1, code2])
        self.assertTrue(self.common.searchDicKV(before_snapshot_json_list[0], 'instrCode') != self.common.searchDicKV(
            before_snapshot_json_list[1], 'instrCode'))
        for info in before_snapshot_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=10))
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (pow(10, 6))) <= start_time_stamp - delay_minute * 60 * 1000 + tolerance_time)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_QuoteOrderBookDataApi_03(self):
        """订阅单市场，多合约的盘口数据，部分合约代码错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HHI2009'
        code2 = 'xxxx'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue('instrument code [ {} ] is unknown'.format(code2) == self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        for info in before_basic_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(int(sourceUpdateTime / (pow(10, 6))) <=
                            start_time_stamp - delay_minute * 60 * 1000)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        for info in before_snapshot_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(int(sourceUpdateTime / (pow(10, 6))) <=
                            start_time_stamp - delay_minute * 60 * 1000)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=10))
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_QuoteOrderBookDataApi_04(self):
        """订阅单市场，多合约的盘口数据，部分市场合约代码为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HHI2009'
        code2 = ''
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))

        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'childType') == 'SUB_ORDER_BOOK')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[0], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'recvReqTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[0], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue('instrument code is null' in self.common.searchDicKV(first_rsp_list[1], 'retMsg'))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'subType') == 'SUB_WITH_MSG_DATA')
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) == start_time_stamp)
        # 响应时间大于接收时间大于请求时间
        self.assertTrue(int(self.common.searchDicKV(first_rsp_list[1], 'rspTimeStamp')) >=
                        int(self.common.searchDicKV(first_rsp_list[1], 'recvReqTimeStamp')) >
                        int(self.common.searchDicKV(first_rsp_list[1], 'startTimeStamp')) - tolerance_time)

        self.logger.debug(u'校验静态数据')
        for info in before_basic_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(int(sourceUpdateTime / (pow(10, 6))) <=
                            start_time_stamp - delay_minute * 60 * 1000)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        for info in before_snapshot_json_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(int(sourceUpdateTime / (pow(10, 6))) <=
                            start_time_stamp - delay_minute * 60 * 1000)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=10))
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code1)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    # --------------------------------------------------订阅逐笔数据----------------------------------------------
    def test_QuoteTradeData_Msg_01(self):
        """ 订阅单个市场、单个合约的逐笔数据"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code = 'HHI2005'
        base_info = [{'exchange': 'HKFE', 'code': code}]
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code)
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(int(sourceUpdateTime / (pow(10, 6))) <=
                            start_time_stamp - delay_minute * 60 * 1000)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_QuoteTradeData_Msg_02(self):
        """ 订阅单个市场、多个合约的逐笔数据"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HHI2009'
        code2 = 'ACC2004'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') in (code1, code2))
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(int(sourceUpdateTime / (pow(10, 6))) <=
                            start_time_stamp - delay_minute * 60 * 1000)  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_QuoteTradeData_Msg_03(self):
        """ 订阅多个合约代码，其中一个code错误"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HHI2009'
        code2 = 'xxxx'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp, recv_num=2))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retMsg') == 'instrument code [ {} ] is unknown'.format(code2))

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据,并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=200))
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            self.assertTrue(self.common.searchDicKV(info, 'instrCode') == code2)  # 仅返回入参正确的code2数据
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
            int(sourceUpdateTime / (pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    # --------------------------------------------------取消订阅start----------------------------------------------------

    # -------------------------------------------------按合约取消订阅-----------------------------------------------------

    def test_UnInstr03(self):
        """订阅多个，取消订阅其中的一个合约"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code1 = 'HHI2005'
        code2 = 'HSI2005'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnInstr04(self):
        """取消订阅单个合约，合约代码与订阅合约代码不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code1 = 'HSI2005'
        code2 = 'HSI2006'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnInstr05(self):
        """订阅多个合约，取消订阅多个合约时，其中多个合约代码与订阅的不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code1 = 'HHI2009'
        code2 = 'HSI2005'
        code3 = 'MCH2006'
        code4 = 'xxxx'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3},
                      {'exchange': 'HKFE', 'code': code4}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnInstr06(self):
        """按合约取消订阅时，code为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code1 = 'HSI2005'
        code2 = ''
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnInstr07(self):
        """按合约取消订阅时，exchange为UNKONWN"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        code = 'HSI2005'
        exchange1 = 'HKFE'
        exchange2 = 'UNKNOWN'
        base_info1 = [{'exchange': exchange1, 'code': code}]
        base_info2 = [{'exchange': exchange2, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    # -----------------------------------------按品种取消订阅-------------------------------------------------
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
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=None, unbase_info=base_info2,
                                                recv_num=100, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

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
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        start_time_stamp = int(time.time() * 1000)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp,
            recv_num=100))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

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
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp,
            recv_num=100))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

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
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp,
            recv_num=50))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

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
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(future=self.api.UnSubsQutoMsgReqApi(
            unsub_type=sub_type, unchild_type=None, unbase_info=base_info2, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    # ------------------------------------------------按市场取消订阅--------------------------------------------------------
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
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
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
                                                start_time_stamp=start_time_stamp, recv_num=2000))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=1000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=1000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=2000))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnMarket_004(self):
        """ 先按合约订阅，再按市场取消订阅"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_INSTR
        child_type = None
        base_info = [{'exchange': 'HKFE', 'code': 'HHI2009'}, {'exchange': 'HKFE', 'code': 'HHI2005'}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
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

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    # ------------------------------------------取消订阅快照数据---------------------------------------------------

    def test_UnSnapshot_003(self):
        """订阅多个合约快照数据，取消订阅部分快照数据"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2005'
        code2 = 'MHI2005'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=20, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnSnapshot_004(self):
        """取消订阅之后，再次发起订阅"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2005'
        code2 = 'MHI2005'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=300, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过接收快照数据的接口，筛选出快照数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        # 再次发起订阅
        start_time_stamp = int(time.time() * 1000)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() > 0)
        for info in before_basic_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'校验前快照数据')
        self.assertTrue(before_snapshot_json_list.__len__() > 0)
        for info in before_snapshot_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            print(int(sourceUpdateTime / (pow(10, 6))), start_time_stamp - delay_minute * 60 * 1000)
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnSnapshot_005(self):
        """订阅一个合约的快照数据，取消订阅时，合约代码与订阅合约代码不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2005'
        code2 = 'HSI2006'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnSnapshot_006(self):
        """订阅一个合约的快照数据，取消订阅时，合约代码错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2005'
        code2 = 'xxx'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp, recv_num=200))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteBasicInfoApi(recv_num=100))
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, sourceUpdateTime)
            self.assertTrue(info == db_json_info)  # 数据与入库记录一致

    def test_UnSnapshot_007(self):
        """订阅多个合约快照数据，取消订阅时部分合约代码与订阅合约代码不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2005'
        code2 = 'MHI2005'
        code3 = 'MCH2012'
        code4 = 'HHI2003'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3},
                      {'exchange': 'HKFE', 'code': code4}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=20, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnSnapshot_008(self):
        """订阅多个合约快照数据，取消订阅时部分合约代码为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2005'
        code2 = 'MHI2005'
        code3 = None
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=200, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnSnapshot_009(self):
        """订阅多个合约快照数据，取消订阅时部分合约代码错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        code1 = 'HHI2005'
        code2 = 'MHI2005'
        code3 = 'xxxxx'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=200, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnSnapshot_011(self):
        """取消订阅快照数据时，exchange传入UNKNOWN"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        exchange = 'HKFE'
        code = 'MHI2005'
        base_info1 = [{'exchange': exchange, 'code': code}]
        base_info2 = [{'exchange': 'UNKNOWN', 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp, recv_num=200))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnSnapshot_012(self):
        """取消订阅快照数据时，code为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_SNAPSHOT
        exchange = 'HKFE'
        code1 = 'MHI2005'
        code2 = None
        base_info1 = [{'exchange': exchange, 'code': code1}]
        base_info2 = [{'exchange': exchange, 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp, recv_num=200))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收快照数据接口，筛选出快照数据，并校验。')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteSnapshotApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_SNAPSHOT, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    # -------------------------------------------------------取消订阅静态数据-------------------------------------------------
    def test_UnQuoteBasicInfo_Msg_004(self):
        """ 先订阅2个合约的静态数据，再取消这2个合约的静态数据，再次订阅"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_BASIC
        code1 = 'HHI2009'
        code2 = 'ACC2005'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 通过调用行情取消订阅接口，取消订阅数据
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 再次订阅静态数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        before_basic_json_list = quote_rsp['before_basic_json_list']

        self.logger.debug(u'校验静态数据')
        self.assertTrue(before_basic_json_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in before_basic_json_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'updateTimestamp'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_BASIC, sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    # ------------------------------------------------取消订阅盘口数据-----------------------------------------------

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
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=200, start_time_stamp=start_time_stamp))
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnQuoteOrderBookDataApi04(self):
        """取消订阅之后，再发起订阅"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HSI2005'
        code2 = 'MHI2005'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=200, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'判断取消订阅之后，是否还会收到盘口数据，如果还能收到，则测试失败')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() == 0)

        # 再次发起订阅
        start_time_stamp = int(time.time() * 1000)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnQuoteOrderBookDataApi05(self):
        """订阅一个合约的盘口数据，取消订阅时，合约代码与订阅合约代码不一致"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HHI2005'
        code2 = 'HSI2006'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=200, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnQuoteOrderBookDataApi06(self):
        """订阅一个合约的盘口数据，取消订阅时，合约代码错误"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        code1 = 'HHI2005'
        code2 = 'xxx'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp, recv_num=200))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')
        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

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
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=200, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

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
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=200, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

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
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=200, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查正确的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnQuoteOrderBookDataApi_11(self):
        """取消订阅盘口数据时，exchange传入UNKNOWN"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        exchange1 = 'HKFE'
        exchange2 = 'UNKNOWN'
        code = 'HHI2005'
        base_info1 = [{'exchange': exchange1, 'code': code}]
        base_info2 = [{'exchange': exchange2, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=500, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnQuoteOrderBookDataApi_012(self):
        """取消订阅盘口数据时，code为空"""
        start_time_stamp = int(time.time() * 1000)
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_ORDER_BOOK
        exchange = 'HKFE'
        code1 = 'MCH2005'
        code2 = ''
        base_info1 = [{'exchange': exchange, 'code': code1}]
        base_info2 = [{'exchange': exchange, 'code': code2}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 取消订阅
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp, recv_num=200))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=300))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    # ------------------------------------------------取消订阅逐笔数据-----------------------------------------------------
    def test_UnQuoteTradeData_Msg_003(self):
        """ 先订阅多个合约的逐笔数据，再取消其中一个合约的逐笔数据"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HHI2005'
        code2 = 'HSI2005'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        # 取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=100, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnQuoteTradeData_Msg_004(self):
        """ 先订阅一个合约的逐笔数据，再取消这个合约的逐笔数据，再次订阅逐笔数据"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HSI2005'
        code2 = 'MHI2005'
        base_info = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        #  取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type, unbase_info=base_info,
                                                recv_num=200, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        # 再次订阅
        self.logger.debug('再次订阅逐笔数据')
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnQuoteTradeData_Msg_005(self):
        """先订阅一个合约的逐笔，取消订阅时合约代码与订阅时的合约代码不一致"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HSI2005'
        code2 = 'MHI2006'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        #  取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=20, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnQuoteTradeData_Msg_006(self):
        """先订阅一个合约的逐笔，取消订阅时合约代码为空"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HSI2005'
        code2 = None
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        before_basic_json_list = quote_rsp['before_basic_json_list']
        before_snapshot_json_list = quote_rsp['before_snapshot_json_list']
        self.assertTrue(before_basic_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(before_snapshot_json_list.__len__() == 0)  # 逐笔订阅不返回静态、快照数据
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        #  取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=200, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnQuoteTradeData_Msg_007(self):
        """先订阅一个合约的逐笔，取消订阅时合约代码错误"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HSI2005'
        code2 = 'xxx'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}]
        base_info2 = [{'exchange': 'HKFE', 'code': code2}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        #  取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=200, start_time_stamp=start_time_stamp))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnQuoteTradeData_Msg_008(self):
        """先订阅多个合约的逐笔，取消订阅时部分合约代码与订阅时的合约代码不一致"""
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HSI2005'
        code2 = 'MHI2005'
        code3 = 'MHI2009'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        #  取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=20, start_time_stamp=start_time_stamp))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnQuoteTradeData_Msg_009(self):
        """先订阅多个合约的逐笔，取消订阅时部分合约代码为空"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HSI2005'
        code2 = 'MHI2005'
        code3 = None
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        #  取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=200, start_time_stamp=start_time_stamp))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')
        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnQuoteTradeData_Msg_010(self):
        """先订阅多个合约的逐笔，取消订阅时部分合约代码错误"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code1 = 'HSI2005'
        code2 = 'MHI2005'
        code3 = 'xxx'
        base_info1 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code2}]
        base_info2 = [{'exchange': 'HKFE', 'code': code1}, {'exchange': 'HKFE', 'code': code3}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        #  取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                recv_num=500, start_time_stamp=start_time_stamp))

        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        self.assertTrue(self.common.searchDicKV(first_rsp_list[1], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnQuoteTradeData_Msg_011(self):
        """ exchange传入UNKNOWN"""
        # 先订阅
        sub_type = SubscribeMsgType.SUB_WITH_MSG_DATA
        child_type = SubChildMsgType.SUB_TRADE_DATA
        code = 'HSI2005'
        base_info1 = [{'exchange': 'HKFE', 'code': code}]
        base_info2 = [{'exchange': 'UNKNOWN', 'code': code}]
        # 通过调用行情订阅接口，订阅数据
        start_time_stamp = int(time.time() * 1000)  # 毫秒时间戳
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        quote_rsp = asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = quote_rsp['first_rsp_list']
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'SUCCESS')

        # 取消订阅
        self.logger.debug('通过调用行情取消订阅接口，取消订阅逐笔数据')
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type,
                                                unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp, recv_num=200))
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收逐笔数据的接口，筛选出逐笔数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteTradeDataApi(recv_num=500))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_TRADE_DATA,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

    def test_UnSubsQutoMsgApi01(self):
        """取消订阅时，sub_type传入UNKNOWN_SUB"""
        start_time_stamp = int(time.time() * 1000)
        sub_type1 = SubscribeMsgType.SUB_WITH_INSTR
        sub_type2 = 'UNKNOWN_SUB'
        exchange = 'HKFE'
        code = 'MCH2005'
        base_info = [{'exchange': exchange, 'code': code}]
        asyncio.get_event_loop().run_until_complete(
            future=self.api.LoginReq(token='xxxx', start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        asyncio.get_event_loop().run_until_complete(
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type1, child_type=None, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type2, unchild_type=None, unbase_info=base_info,
                                                start_time_stamp=start_time_stamp, recv_num=200))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

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
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type1, child_type=None, base_info=base_info1,
                                              start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type2, unchild_type=None, unbase_info=base_info2,
                                                start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

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
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type1, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type2,
                                                unbase_info=base_info,
                                                recv_num=50, start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致

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
            future=self.api.DelaySubsQutoMsgReqApi(sub_type=sub_type, child_type=child_type1, base_info=base_info,
                                              start_time_stamp=start_time_stamp))
        asyncio.run_coroutine_threadsafe(self.api.hearbeat_job(), self.new_loop)
        first_rsp_list = asyncio.get_event_loop().run_until_complete(
            future=self.api.UnSubsQutoMsgReqApi(unsub_type=sub_type, unchild_type=child_type2,
                                                unbase_info=base_info,
                                                start_time_stamp=start_time_stamp))

        self.logger.debug(u'通过调用行情订阅接口，订阅数据，并检查错误的返回结果')
        self.assertTrue(self.common.searchDicKV(first_rsp_list[0], 'retCode') == 'FAILURE')

        self.logger.debug(u'通过接收盘口数据的接口，筛选出盘口数据并校验')
        info_list = asyncio.get_event_loop().run_until_complete(future=self.api.QuoteOrderBookDataApi(recv_num=100))
        self.assertTrue(info_list.__len__() > 0)
        start_time_stamp = int(time.time() * 1000)  # 毫秒级
        for info in info_list:
            instrCode = self.common.searchDicKV(info, 'instrCode')
            sourceUpdateTime = int(self.common.searchDicKV(info, 'sourceUpdateTime'))
            self.assertTrue(
                int(sourceUpdateTime / (
                    pow(10, 6))) <= (start_time_stamp - delay_minute * 60 * 1000 + tolerance_time))  # 毫秒级别对比，延迟delay_minute分钟
            db_json_info = self.api.sq.get_subscribe_record(instrCode, QuoteMsgType.PUSH_ORDER_BOOK,
                                                            sourceUpdateTime)
            self.assertTrue(self.common.compareSubData(info, db_json_info))  # 数据与入库记录一致
    # --------------------------------------------------取消订阅end----------------------------------------------------


if __name__ == '__main_':
    unittest.main()
