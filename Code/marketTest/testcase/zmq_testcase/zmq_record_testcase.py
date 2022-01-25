# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/4/14
# @Software: PyCharm

import unittest
from py_sqlite.base_sql import *
from common.test_log.ed_log import get_log
from common.pb_method import k_type_convert, exchange_convert


class CheckZMQ(unittest.TestCase):
    def __init__(self, methodName='runTest', check_json_list=None, is_before_data=False, sub_time=None, start_time=None, instr_code=None, exchange=None, peroid_type=None):
        super().__init__(methodName)
        self.check_json_list = check_json_list
        self.is_before_data = is_before_data
        self.sub_time = sub_time
        self.start_time = start_time
        self.instr_code = instr_code
        self.exchange = exchange
        self.peroid_type = peroid_type
        self.logger = get_log()
        self.tolerance_time = 30000

    @classmethod
    def setUpClass(cls):
        cls.sq = SqliteDB()
        cls.common = Common()

    @classmethod
    def tearDownClass(cls):
        cls.sq.exit()

    # --------------------------------------------采集服务start----------------------------------------------------
    def test_01_QuoteSnapshot(self):
        if self.check_json_list is None:
            check_info = self.sq.get_pub_json_records('56', 10000)
        else:
            check_info = self.check_json_list
        self.assertTrue(check_info.__len__() >= 1)
        self.logger.debug('{} items to check!'.format(check_info.__len__()))
        assert_json = {'instrCodeList': []}
        for info in check_info:
            if self.check_json_list is None:
                record_time = info[1]
                json_info = json.loads(info[0])
            else:
                record_time = int(time.time())  # 因是实时传入，所以可以取当前时间
                json_info = info
            self.logger.debug(json_info)
            commonInfo = json_info['commonInfo']
            exchange = commonInfo['exchange']
            productCode = commonInfo['productCode']
            instrCode = commonInfo['instrCode']
            precision = self.common.doDicEvaluate(commonInfo, 'precision')
            collectorRecvTime = commonInfo['collectorRecvTime']
            collectorSendTime = commonInfo['collectorSendTime']
            if self.check_json_list is not None:
                publisherRecvTime = commonInfo['publisherRecvTime']
                publisherSendTime = commonInfo['publisherSendTime']
                self.assertTrue(int(publisherSendTime) >= int(publisherRecvTime))  # 订阅服务发出时间大于采集接受时间
            close = json_info['close']
            if 'open' in json_info.keys():  # 存在未成交数据但是有快照的情况
                open = int(json_info['open'])
                high = int(json_info['high'])
                low = int(json_info['low'])
                last = int(json_info['last'])
                # normal = json_info['normal']
                # volume = int(json_info['volume'])
                self.assertTrue(int(high) >= int(open) >= int(low))  # 开盘价在最高价最低价之间
                self.assertTrue(int(high) >= int(last) >= int(low))  # 最新现价在最高价最低价之间
            riseFall = int(self.common.doDicEvaluate(json_info, 'riseFall'))
            rFRatio = int(self.common.doDicEvaluate(json_info, 'rFRatio'))
            # localDateTime = json_info['localDateTime']
            sourceUpdateTime = int(json_info['sourceUpdateTime'])
            future = json_info['future']
            openInterrest = self.common.doDicEvaluate(future, 'openInterrest')
            settlementPrice = self.common.doDicEvaluate(future, 'settlementPrice')
            self.assertTrue(int(collectorRecvTime) < int(collectorSendTime))  # 采集发出时间大于采集接受时间

            #  判断外盘期货12点之前和12点之后的日期
            if exchange != 'HKFE' and record_time <= self.common.getTwelveHourStamp():
                self.assertTrue(self.common.isTimeInYesterday(sourceUpdateTime))  # 更新时间是否是昨天的数据
            else:
                self.assertTrue(self.common.isTimeInToday(sourceUpdateTime))  # 更新时间是否是今天的数据
            if exchange != 'HKFE':
                if self.sub_time:
                    self.logger.debug('check sub_time is:{}'.format(self.sub_time))
                    if not self.is_before_data:  # 实时数据
                        self.assertTrue(int(sourceUpdateTime) / (pow(10, 6)) + (60 * 60 * 12 * 1000) >= int(
                            self.sub_time))  # 订阅服务时用来判断订阅时间与源时间
                    else:
                        self.assertTrue(int(sourceUpdateTime) / (pow(10, 6)) + (60 * 60 * 12 * 1000) <= int(
                            self.sub_time))  # 订阅服务时用来判断订阅时间与源时间
                else:
                    pass
            else:
                if self.sub_time:
                    self.logger.debug('check sub_time is:{}'.format(self.sub_time))
                    if not self.is_before_data:  # 实时数据
                        self.assertTrue(int(sourceUpdateTime) / (pow(10, 6)) >= int(
                            self.sub_time))  # 订阅服务时用来判断订阅时间与源时间
                    else:
                        self.assertTrue(int(sourceUpdateTime) / (pow(10, 6)) <= int(
                            self.sub_time))  # 订阅服务时用来判断订阅时间与源时间
                else:
                    pass
                # 更新时间应该是有序的
            if not self.is_before_data:
                if exchange + '_sourceUpdateTime' in assert_json.keys():
                    self.assertTrue(int(sourceUpdateTime) >= int(assert_json[exchange + '_sourceUpdateTime']))
                    assert_json[exchange + '_sourceUpdateTime'] = int(sourceUpdateTime)
                else:
                    assert_json[exchange + '_sourceUpdateTime'] = int(sourceUpdateTime)
            else:
                pass
            # 校验涨跌额涨跌幅的计算逻辑
            if 'open' in json_info.keys():  # 存在未成交数据但是有快照的情况
                if settlementPrice:
                    self.assertTrue(int(riseFall) == int(last) - int(settlementPrice))
                    self.assertTrue(int(rFRatio) == int(10000 * int(riseFall) / int(settlementPrice)))
                else:
                    self.assertTrue(int(riseFall) == int(last) - int(close))
                    self.assertTrue(int(rFRatio) == int(10000 * int(riseFall) / int(close)))
            if instrCode in assert_json['instrCodeList']:
                # self.assertTrue(int(volume) >= int(assert_json[instrCode + '_volume']))  # 当天成交量应该是递增的
                # assert_json[instrCode + '_volume'] = int(volume)
                self.assertTrue(int(open) == int(assert_json[instrCode + '_open']))  # 当天开盘价不会再更新
                self.assertTrue(int(close) == int(assert_json[instrCode + '_close']))  # 当天昨收价不会再更新
                self.assertTrue(int(settlementPrice) == int(assert_json[instrCode + '_settlementPrice']))  # 当天昨结价不会再更新
                self.assertTrue(int(openInterrest) == int(assert_json[instrCode + '_openInterrest']))  # 当天昨持仓量不会再更新
                if int(last) > assert_json[instrCode + '_high']:
                    self.assertTrue(int(high) == int(last))  # 最高价应更新
                    assert_json[instrCode + '_high'] = int(high)
                else:
                    self.assertTrue(int(high) == int(assert_json[instrCode + '_high']))  # 最高价不更新
                if last < assert_json[instrCode + '_low']:
                    self.assertTrue(int(low) == int(last))  # 最低价应更新
                    assert_json[instrCode + '_low'] = int(low)
                else:
                    self.assertTrue(int(low) == int(assert_json[instrCode + '_low']))  # 最低价不更新
            else:
                if 'open' in json_info.keys():  # 存在未成交数据但是有快照的情况
                    assert_json['instrCodeList'].append(instrCode)
                    # assert_json[instrCode + '_volume'] = int(volume)
                    assert_json[instrCode + '_open'] = int(open)
                    assert_json[instrCode + '_close'] = int(close)
                    assert_json[instrCode + '_settlementPrice'] = int(settlementPrice)
                    assert_json[instrCode + '_high'] = int(high)
                    assert_json[instrCode + '_low'] = int(low)
                    assert_json[instrCode + '_openInterrest'] = int(openInterrest)

    def test_02_QuoteOrderBookData(self):
        if self.check_json_list is None:
            check_info = self.sq.get_pub_json_records('57', 10000)
        else:
            check_info = self.check_json_list
        self.assertTrue(check_info.__len__() >= 1)
        self.logger.debug('{} items to check!'.format(check_info.__len__()))
        assert_json = {'instrCodeList': []}
        for info in check_info:
            if self.check_json_list is None:
                record_time = info[1]
                json_info = json.loads(info[0])
            else:
                record_time = int(time.time())  # 因是实时传入，所以可以取当前时间
                json_info = info
            self.logger.debug(json_info)
            commonInfo = json_info['commonInfo']
            exchange = commonInfo['exchange']
            productCode = commonInfo['productCode']
            instrCode = commonInfo['instrCode']
            # 有些精度为0时，无返回
            precision = self.common.doDicEvaluate(commonInfo, 'precision')
            collectorRecvTime = commonInfo['collectorRecvTime']
            collectorSendTime = commonInfo['collectorSendTime']
            if self.check_json_list is not None:
                publisherRecvTime = commonInfo['publisherRecvTime']
                publisherSendTime = commonInfo['publisherSendTime']
                self.assertTrue(int(publisherSendTime) >= int(publisherRecvTime))  # 订阅服务发出时间大于采集接受时间
            orderBook = json_info['orderBook']
            sourceUpdateTime = json_info['sourceUpdateTime']
            #  判断外盘期货12点之前和12点之后的日期
            if exchange != 'HKFE' and record_time <= self.common.getTwelveHourStamp():
                self.assertTrue(self.common.isTimeInYesterday(sourceUpdateTime))  # 更新时间是否是昨天的数据
            else:
                self.assertTrue(self.common.isTimeInToday(sourceUpdateTime))  # 更新时间是否是今天的数据
            if exchange != 'HKFE':
                if self.sub_time:
                    self.logger.debug('check sub_time is:{}'.format(self.sub_time))
                    if not self.is_before_data:  # 实时数据
                        self.assertTrue(int(sourceUpdateTime) / (pow(10, 6)) + (60 * 60 * 12 * 1000) >= int(
                            self.sub_time))  # 订阅服务时用来判断订阅时间与源时间
                    else:
                        self.assertTrue(int(sourceUpdateTime) / (pow(10, 6)) + (60 * 60 * 12 * 1000) <= int(
                            self.sub_time))  # 订阅服务时用来判断订阅时间与源时间
                else:
                    pass
            else:
                if self.sub_time:
                    self.logger.debug('check sub_time is:{}'.format(self.sub_time))
                    if not self.is_before_data:     # 实时数据
                        self.assertTrue(int(sourceUpdateTime) / (pow(10, 6)) >= int(
                            self.sub_time))  # 订阅服务时用来判断订阅时间与源时间
                    else:
                        self.assertTrue(int(sourceUpdateTime) / (pow(10, 6)) <= int(
                            self.sub_time))  # 订阅服务时用来判断订阅时间与源时间
                else:
                    pass
                # 更新时间应该是有序的
            if not self.is_before_data:
                if exchange + '_sourceUpdateTime' in assert_json.keys():
                    self.assertTrue(int(sourceUpdateTime) >= int(assert_json[exchange + '_sourceUpdateTime']))
                    assert_json[exchange + '_sourceUpdateTime'] = int(sourceUpdateTime)
                else:
                    assert_json[exchange + '_sourceUpdateTime'] = int(sourceUpdateTime)
            else:
                pass
            self.assertTrue(int(collectorRecvTime) < int(collectorSendTime))  # 采集发出时间大于采集接受时间
            askVolInData, bidVolInData, upperAskPrice, upperBidPrice = 0, 0, 0, 0
            if 'askVol' in orderBook.keys():
                askVol = int(orderBook['askVol'])
                asksData = orderBook['asksData']
                self.assertTrue(asksData.__len__() == 10)  # 卖盘10层深度
                for ask in asksData:
                    if ask != {}:
                        askPrice = int(ask['price'])
                        askVolume = int(ask['volume'])
                        if exchange == 'SGX':  # 新加坡时orderCount值为0在protobuf中打印不出，不做校验
                            pass
                        else:
                            askOrderCount = ask['orderCount']
                        askVolInData = askVolInData + askVolume
                        if upperAskPrice:
                            self.assertTrue(int(askPrice) > int(upperAskPrice))  # 深度价格校验（卖1价格应低于卖2价格）
                        upperAskPrice = askPrice
                self.assertEqual(int(askVol), askVolInData)  # 校验卖盘数量和
            if 'bidVol' in orderBook.keys():
                bidVol = int(orderBook['bidVol'])
                bidsData = orderBook['bidsData']
                self.assertTrue(bidsData.__len__() == 10)  # 买盘10层深度
                for bid in bidsData:
                    if bid != {}:
                        bidPrice = int(bid['price'])
                        bidVolume = int(bid['volume'])
                        if exchange == 'SGX':  # 新加坡时orderCount值为0在protobuf中打印不出，不做校验
                            pass
                        else:
                            bidOrderCount = bid['orderCount']
                        bidVolInData = bidVolInData + bidVolume
                        if upperBidPrice:
                            self.assertTrue(int(bidPrice) < int(upperBidPrice))  # 深度价格校验（买1价格应高于买2价格）
                        upperBidPrice = bidPrice
                self.assertEqual(int(bidVol), bidVolInData)  # 校验买盘数量和

    def test_03_QuoteBasicInfo(self):   # 推送的静态数据
        if self.check_json_list == None:
            check_info = self.sq.get_pub_json_records('55', 100)
        else:
            check_info = self.check_json_list
        self.assertTrue(check_info.__len__() >= 1)
        self.logger.debug('{} items to check!'.format(check_info.__len__()))
        for info in check_info:
            if self.check_json_list == None:
                record_time = info[1]
                json_info = json.loads(info[0])
            else:
                record_time = int(time.time())  # 因是实时传入，所以可以取当前时间
                json_info = info
            self.logger.debug(json_info)
            commonInfo = json_info['commonInfo']
            exchange = commonInfo['exchange']
            productCode = commonInfo['productCode']
            instrCode = commonInfo['instrCode']
            sourceUpdateTime = int(json_info['updateTimestamp'])
            # 有些精度为0时，无返回
            precision = self.common.doDicEvaluate(commonInfo, 'precision')
            collectorRecvTime = commonInfo['collectorRecvTime']
            collectorSendTime = commonInfo['collectorSendTime']
            if self.check_json_list != None:
                publisherRecvTime = commonInfo['publisherRecvTime']
                publisherSendTime = commonInfo['publisherSendTime']
                self.assertTrue(int(publisherSendTime) >= int(publisherRecvTime))  # 订阅服务发出时间大于采集接受时间
            type = json_info['type']
            tradindDay = json_info['tradindDay']
            if exchange != 'HKFE' and record_time <= self.common.getTwelveHourStamp():  # 获取数据在12点之前的交易日为上一交易日，12点之后获取的数据交易日与当日相同
                self.assertTrue(self.common.inYesterday(tradindDay))
                self.assertTrue(self.common.isTimeInYesterday(sourceUpdateTime))  # 更新时间是否是昨天的数据
            elif exchange == 'HKFE' and record_time >= self.common.getNextHKFEStartStamp():
                self.assertTrue(self.common.isTomorrow(tradindDay))
                self.assertTrue(self.common.isTimeInToday(sourceUpdateTime))  # 更新时间是否是当天的数据
            else:
                self.assertTrue(self.common.inToday(tradindDay))
                self.assertTrue(self.common.isTimeInToday(sourceUpdateTime))  # 更新时间是否是今天的数据

            if exchange != 'HKFE':
                if self.sub_time:
                    self.logger.debug('check sub_time is:{}'.format(self.sub_time))
                    self.assertTrue(
                        int(sourceUpdateTime) / (pow(10, 6)) + (60 * 60 * 12 * 1000) <= int(
                            self.sub_time))  # 订阅服务时用来判断订阅时间与源时间
                else:
                    pass
            else:
                if self.sub_time:
                    self.logger.debug('check sub_time is:{}'.format(self.sub_time))
                    self.assertTrue(int(sourceUpdateTime) / (pow(10, 6)) <= int(
                        self.sub_time))  # 订阅服务时用来判断订阅时间与源时间
                else:
                    pass
            # instrName = json_info['instrName'] # 合约名称和合约英文名，在合约信息里获取，静态数据里不填。
            # instrEnName = json_info['instrEnName'] # 合约名称和合约英文名，在合约信息里获取，静态数据里不填。
            exchangeInstr = json_info['exchangeInstr']
            marketStatus = json_info['marketStatus']
            instrStatus = json_info['instrStatus']
            # precision = json_info['precision']
            # upperLimit = json_info['upperLimit']
            # lowerLimit = json_info['lowerLimit']
            # preClose = json_info['preClose']
            source = json_info['source']
            # updateTime = json_info['updateTime']   # 开发在jira评论 update_time不填
            # future = json_info['future']       # 开发在jira评论, 暂时无法做到
            # preSettlementPrice = future['preSettlementPrice']
            # preOpenInterrest = future['preOpenInterrest']
            self.assertTrue(int(collectorSendTime) >= int(collectorRecvTime))  # 采集发出时间大于采集接受时间
            self.assertTrue(productCode in instrCode)  # 产品代码正确性校验



    def test_03_01_QuoteBasicInfo(self):  # dealer模式下请求返回的静态数据
        if self.check_json_list == None:
            check_info = self.sq.get_deal_json_records('65', 100)
        else:
            check_info = self.check_json_list
        self.assertTrue(check_info.__len__() >= 1)
        self.logger.debug('{} items to check!'.format(check_info.__len__()))
        for info in check_info:
            if self.check_json_list == None:
                record_time = info[1]
                json_info = json.loads(info[0])
            else:
                record_time = int(time.time())  # 因是实时传入，所以可以取当前时间
                json_info = info
            # self.logger.debug(json_info)
            retResult = json_info['retResult']
            retCode = retResult['retCode']
            self.assertTrue(retCode == 'SUCCESS')  # 校验接口返回状态
            basicInfos = json_info['basicInfos']
            self.logger.debug('{} basicInfos to check!'.format(basicInfos.__len__()))
            for basicInfo in basicInfos:
                self.logger.debug(basicInfo)
                commonInfo = basicInfo['commonInfo']
                exchange = commonInfo['exchange']
                productCode = commonInfo['productCode']
                instrCode = commonInfo['instrCode']
                precision = self.common.doDicEvaluate(commonInfo, 'precision', 0)
                collectorRecvTime = commonInfo['collectorRecvTime']
                collectorSendTime = commonInfo['collectorSendTime']
                if self.check_json_list != None:
                    publisherRecvTime = commonInfo['publisherRecvTime']
                    publisherSendTime = commonInfo['publisherSendTime']
                    self.assertTrue(int(publisherSendTime) >= int(publisherRecvTime))  # 订阅服务发出时间大于采集接受时间
                type = basicInfo['type']
                tradind_day = basicInfo['tradindDay']
                if exchange != 'HKFE' and record_time <= self.common.getTwelveHourStamp():#获取数据在12点之前的交易日为上一交易日，12点之后获取的数据交易日与当日相同
                    self.assertTrue(self.common.inYesterday(tradind_day))
                else:
                    self.assertTrue(self.common.inToday(tradind_day))
                instr_name = basicInfo['instrName']
                instr_en_name = basicInfo['instrEnName']
                exchange_instr = basicInfo['exchangeInstr']
                market_status = basicInfo['marketStatus']
                instr_status = basicInfo['instrStatus']
                source = basicInfo['source']
                update_timestamp = basicInfo['updateTimestamp']
                self.assertTrue(int(collectorSendTime) >= int(collectorRecvTime))  # 采集发出时间大于采集接受时间
                self.assertTrue(productCode in instrCode)  # 产品代码正确性校验
                self.assertTrue(instrCode == exchange_instr)  # 代码正确性校验
                future = basicInfo['future']
                pre_settlement_price = future['preSettlementPrice']#会出现一些合约确实是没有值的情况，所以根据情况校验
                pre_open_interrest = future['preOpenInterrest']

    def test_04_QuoteTradeData(self):
        if self.check_json_list == None:
            check_info = self.sq.get_pub_json_records('58', 1000000)
        else:
            check_info = self.check_json_list
        self.assertTrue(check_info.__len__() >= 1)
        self.logger.debug('{} items to check!'.format(check_info.__len__()))
        assert_json = {
            'instrCodeList': [],
        }
        for info in check_info:
            if self.check_json_list == None:
                record_time = info[1]
                json_info = json.loads(info[0])
            else:
                record_time = int(time.time())  # 因是实时传入，所以可以取当前时间
                json_info = info
            self.logger.debug(json_info)
            commonInfo = json_info['commonInfo']
            exchange = commonInfo['exchange']
            instrCode = commonInfo['instrCode']
            # 有些精度为0时，无返回
            precision = self.common.doDicEvaluate(commonInfo, 'precision')
            if not self.is_before_data:    # 历史数据无该字段
                productCode = commonInfo['productCode']
                self.assertTrue(productCode in instrCode)
                collectorRecvTime = commonInfo['collectorRecvTime']
                collectorSendTime = commonInfo['collectorSendTime']
                if self.check_json_list != None:
                    publisherRecvTime = commonInfo['publisherRecvTime']
                    publisherSendTime = commonInfo['publisherSendTime']
                    self.assertTrue(int(publisherSendTime) >= int(publisherRecvTime))  # 订阅服务发出时间大于采集接受时间
                    self.assertTrue(int(collectorRecvTime) < int(collectorSendTime))  # 采集发出时间大于采集接受时间
            else:
                pass
            tradeTick = json_info['tradeTick']
            price = int(tradeTick['price'])
            vol = int(tradeTick['vol'])
            trade_time = int(tradeTick['time'])
            direct = tradeTick['direct']
            # future = tradeTick['future'] # 目前行情源取不到此字段，不填
            sourceUpdateTime = trade_time
            if exchange != 'HKFE' and record_time <= self.common.getTwelveHourStamp():
                self.assertTrue(self.common.isTimeInYesterday(sourceUpdateTime))  # 更新时间是否是昨天的数据
            else:
                self.assertTrue(self.common.isTimeInToday(sourceUpdateTime))  # 更新时间是否是今天的数据

            if exchange != 'HKFE':
                if self.sub_time:
                    self.logger.debug('check sub_time is:{}'.format(self.sub_time))
                    if not self.is_before_data:  # 实时数据
                        self.assertTrue(int(sourceUpdateTime) / (pow(10, 6)) + (60 * 60 * 12 * 1000) >= int(
                            self.sub_time))  # 订阅服务时用来判断订阅时间与源时间
                    else:
                        self.assertTrue(int(sourceUpdateTime) / (pow(10, 6)) + (60 * 60 * 12 * 1000) <= int(
                            self.sub_time))  # 订阅服务时用来判断订阅时间与源时间
                else:
                    pass
            else:
                if self.sub_time:
                    self.logger.debug('check sub_time is:{}'.format(self.sub_time))
                    if not self.is_before_data:     # 实时数据
                        self.assertTrue(int(sourceUpdateTime) / (pow(10, 6)) >= int(
                            self.sub_time))  # 订阅服务时用来判断订阅时间与源时间
                    else:
                        self.assertTrue(int(sourceUpdateTime) / (pow(10, 6)) <= int(
                            self.sub_time))  # 订阅服务时用来判断订阅时间与源时间
                else:
                    pass
            if 'sourceUpdateTime' in assert_json.keys():
                # 更新时间应该是有序的
                if exchange + '_sourceUpdateTime' in assert_json.keys():
                    self.assertTrue(int(sourceUpdateTime) >= int(assert_json[exchange + '_sourceUpdateTime']))
                    assert_json[exchange + '_sourceUpdateTime'] = int(sourceUpdateTime)
                else:
                    assert_json[exchange + '_sourceUpdateTime'] = int(sourceUpdateTime)


            # if instrCode in assert_json['instrCodeList'] and 'main' not in instrCode:
            if instrCode in assert_json['instrCodeList']:
                if price > assert_json[instrCode]:
                    assert_json[instrCode] = price  # 更新价格
                    self.assertTrue(direct == 'BUY')
                elif price < assert_json[instrCode]:
                    assert_json[instrCode] = price  # 更新价格
                    self.assertTrue(direct == 'SELL')
                else:
                    assert_json[instrCode] = price  # 更新价格
                    self.assertTrue(direct == 'NO_STATE')
            else:
                assert_json['instrCodeList'].append(instrCode)
                assert_json[instrCode] = price
        self.logger.debug('{} items checked!'.format(check_info.__len__()))

    def test_04_APP_BeforeQuoteTradeData(self):
        check_info = self.check_json_list
        self.assertTrue(check_info.__len__() >= 1)
        self.logger.debug('{} items to check!'.format(check_info.__len__()))
        exchange = 'noExchange'
        instrCode = 'noInstrCode'
        assert_json = {
            'instrCodeList': [],
        }
        for info in check_info:
            record_time = int(time.time())  # 因是实时传入，所以可以取当前时间
            json_info = info
            self.logger.debug(json_info)
            price = int(json_info['price'])
            vol = int(json_info['vol'])
            trade_time = int(json_info['time']) / pow(10, 6)
            direct = json_info['direct']
            # 得到数据的数据应在查询时间之间
            self.assertTrue(self.start_time <= trade_time <= self.sub_time)
            # 更新时间应该是有序的
            if exchange + '_sourceUpdateTime' in assert_json.keys():
                self.assertTrue(int(trade_time) >= int(assert_json[exchange + '_sourceUpdateTime']))
                assert_json[exchange + '_sourceUpdateTime'] = int(trade_time)
            else:
                assert_json[exchange + '_sourceUpdateTime'] = int(trade_time)

            if instrCode in assert_json['instrCodeList']:
                if price > assert_json[instrCode]:
                    assert_json[instrCode] = price  # 更新价格
                    self.assertTrue(direct == 'BUY')
                elif price < assert_json[instrCode]:
                    assert_json[instrCode] = price  # 更新价格
                    self.assertTrue(direct == 'SELL')
                else:
                    assert_json[instrCode] = price  # 更新价格
                    self.assertTrue(direct == 'NO_STATE')
            else:
                assert_json['instrCodeList'].append(instrCode)
                assert_json[instrCode] = price

    def test_05_InstrumentInfo(self):
        if self.check_json_list == None:
            check_info = self.sq.get_deal_json_records('10', 100)
        else:
            check_info = self.check_json_list
        self.assertTrue(check_info.__len__() >= 1)
        self.logger.debug('{} items to check!'.format(check_info.__len__()))
        for info in check_info:
            if self.check_json_list == None:
                record_time = info[1]
                json_info = json.loads(info[0])
            else:
                record_time = int(time.time())  # 因是实时传入，所以可以取当前时间
                json_info = info
            self.logger.debug(json_info)
            retResult = json_info['retResult']
            retCode = retResult['retCode']
            self.assertTrue(retCode == 'SUCCESS')  # 校验接口返回状态
            instruments = json_info['instruments']
            self.logger.debug('{} instruments to check!'.format(instruments.__len__()))
            for instrument in instruments:
                self.logger.debug(instrument)
                base = instrument['base']
                instrType = base['instrType']
                exchange = base['exchange']
                # seriesId = base['seriesId']
                internalCode = base['internalCode']
                if internalCode[-1:] in {'W', 'Y'}:
                    pass
                else:
                    instrCode = base['instrCode']
                    counterCode = base['counterCode']
                # cn_simple_name =base ['cnSimpleName']
                # tc_simple_name =base['tcSimpleName']
                # en_simple_name = base['enSimpleName']
                # cn_full_name = base['cnFullName']
                # tc_full_name = base['tcFullName']
                # en_full_name = base['enFullName']
                proc = instrument['proc']
                categoryType = proc['categoryType']
                productType = proc['productType']
                code = proc['code']
                # prod_cn_simple_name = proc['cnSimpleName']
                # prod_tc_simple_name = proc['tcSimpleName']
                # prod_en_simple_name = proc['enSimpleName']
                # prod_cn_full_name = proc['cnFullName']
                # prod_tc_full_name = proc['tcFullName']
                # prod_en_full_name = proc['enFullName']
                # self.assertEqual(cn_simple_name,prod_cn_simple_name)
                # self.assertEqual(tc_simple_name,prod_tc_simple_name)
                # self.assertEqual(en_simple_name,prod_en_simple_name)
                # self.assertEqual(cn_full_name, prod_cn_full_name)
                # self.assertEqual(tc_full_name, prod_tc_full_name)
                # self.assertEqual(en_full_name, prod_en_full_name)
                # timespin = proc['timespin']
                callMarket = self.common.doDicEvaluate(proc, 'callMarket', 2)  # 集合竞价时间片,有的品种没有集合竞价
                # trade = proc['trade']  # 交易时间片
                # denoinator = self.common.doDicEvaluate(instrument, 'denoinator', 0)  # ？？为啥有的没有    外期也没有这个字段
                precision = self.common.doDicEvaluate(instrument, 'precision', 0)
                status = instrument['status']
                # createDate = instrument['createDate']     # 取不到
                # openDate = instrument['openDate']     # 取不到
                updateStamp = instrument['updateStamp']       # 港期取不到     外期可以取到
                timeZone = instrument['timeZone']
                future = instrument['future']

                # marginRateType = future['marginRateType']
                # longMargin = future['longMargin']
                # shortMargin = future['shortMargin']
                # marketOrderQty = future['marketOrderQty']
                # limitOrderQty = future['limitOrderQty']
                # deliverYear = future['deliverYear']
                # deliverMonth = future['deliverMonth']
                is_master_instr = self.common.doDicEvaluate(instrument, 'isMasterInstr', 0)#不是主力合约的时候是不会有这个字段的
                if is_master_instr!=0:
                    isMasterInstr = future['isMasterInstr']
                    relatedInstr = future['relatedInstr']
                # lastTradeDate = future['lastTradeDate']
                # notifyDate = future['notifyDate']
                expireDate = future['expireDate']
                if int(expireDate) < int(time.strftime('%Y%m%d', time.localtime())): # 校验到期日是否为过期的，过期的不需要校验结算、交易币种
                    self.assertEqual(status,'EXPIRED')
                else:#未过期的时候需要有以下字段
                    settleCurrency = base['settleCurrency']
                    tradeCurrency = base['tradeCurrency']
                    isEnable = future['isEnable']
                    tradeAble = instrument['tradeAble']
                    self.assertEqual(str(isEnable),'True')
                    self.assertEqual(str(tradeAble),'True')
                # beginDeliverDate = future['beginDeliverDate']
                # endDeliverDate = future['endDeliverDate']

                # timespin = timespin.rstrip(' ')
                # timespinList = re.findall('(\d+-\d+) ?', timespin)
                # assert_list = trade + callMarket  # timespin字段是由交易时间和竞价时间组合得到的
                # start_list = [assert_list[j]['start'] for j in range(assert_list.__len__())]
                # end_list = [assert_list[k]['end'] for k in range(assert_list.__len__())]
                # for i in range(timespinList.__len__()):  # 校验时间片与交易时间、竞价时间的匹配性
                #     self.assertTrue(str(start_list[i]) in str(timespinList[i]))
                #     self.assertTrue(str(end_list[i]) in str(timespinList[i]))

                # 校验交易状态bug：休市时依然返回trading
                # if self.common.isInTradeTime(record_time, trade) or self.common.isInTradeTime(record_time, callMarket):
                #     self.assertTrue(status == 'TRADING')
                #     self.assertTrue(tradeAble == True)
                # else:
                #     self.assertTrue(status != 'TRADING')
                #     self.assertTrue(tradeAble == False)
                # self.assertTrue(instrCode == code + seriesId)
                # self.assertTrue(counterCode == code + seriesId)
                if exchange != 'HKFE':
                    self.assertTrue(timeZone == 'EST')
                else:
                    self.assertTrue(timeZone == 'CCT')
                # 这些code在港交所、外期里面没有找到，先跳过

                # if instrCode in {'6B2010','6C2010','6A2010','NIY2010','SI2008','6J2010','6E2010'}:#外期时这几个合约获取不到后面的字段，需单个排除
                #     pass
                # else:
                lotSize = instrument['lotSize']
                priceTick = instrument['priceTick']
                contractMultiplier = future['contractMultiplier']
                if code not in ['LUA', 'LUN', 'LUZ', 'HB1', 'HHN', 'LUP', 'VHS', 'HHT', 'BOV', 'HSN', 'LUC', 'HB3',
                                'LUS', 'SAF', 'UIN', 'YZA', 'CIN', 'HST', 'MCX', '6N', 'E7', 'J7', 'NQ', 'MNQ', 'ES',
                                'MES', 'NIY', 'CL', 'YM', 'NK', 'TW', 'CN']:
                    lotSizeAndContractMultiplier = self.common.getFutureLotSizeAndContractMultiplier(code)
                    self.assertTrue(
                        int(lotSize) == int(lotSizeAndContractMultiplier['lotSize']))  # 与港交所公开数据对比合约规模字段的准确性
                    self.assertTrue(int(contractMultiplier) == int(
                        lotSizeAndContractMultiplier['contractMultiplier']))  # 与港交所公开数据对比合约数量乘数字段的准确性

    # --------------------------------------------采集服务end----------------------------------------------------

    # --------------------------------------------计算服务start-------------------------------------------------
    def test_06_PushKLineMinData(self):
        # 推送分时K线
        peroidType = 'MIN'
        if self.check_json_list == None:
            check_info = self.sq.get_pub_json_records('61', 1000000)
        else:
            check_info = self.check_json_list
        self.assertTrue(check_info.__len__() >= 1)
        self.logger.debug('{} items to check!'.format(check_info.__len__()))
        assert_json = {}
        if self.is_before_data:
            first_time = self.common.searchDicKV(check_info[0], 'updateDateTime')
            if self.exchange == 'HKFE':
                self.assertTrue(first_time[-6:] == '171600')    # 港期夜盘下午5.15开盘
            else:
                self.assertTrue(first_time[-6:] == '170100')    # 外期夜盘下午5.00开盘
        else:
            pass
        for info in check_info:
            if self.check_json_list == None:
                record_time = info[1]
                json_info = json.loads(info[0])
            else:
                record_time = int(time.time())  # 因是实时传入，所以可以取当前时间
                json_info = info
            self.logger.debug(json_info)
            if not self.is_before_data:    # 实时push
                exchange = json_info['exchange']
                code = json_info['code']
                data = json_info['data'][0]
                if self.check_json_list == None:
                    get_info = json.loads(check_info[-1][0])
                    latest_time = get_info['data'][0]['updateDateTime']
                else:
                    latest_time = check_info[-1]['data'][0]['updateDateTime']
            else:   # app订阅的历史数据直接返回data list，不返回exchange、code字段
                exchange = self.exchange
                code = self.instr_code
                data = json_info
                latest_time = self.common.searchDicKV(check_info[-1], 'updateDateTime')
            latest_time_stamp = int(time.mktime(time.strptime(latest_time, "%Y%m%d%H%M%S"))) * 1000
            high = int(data['high'])
            open = int(data['open'])
            low = int(data['low'])
            close = int(data['close'])
            # average = int(data['average'])
            vol = int(self.common.doDicEvaluate(data, 'vol'))
            riseFall = int(self.common.doDicEvaluate(data, 'riseFall'))
            rFRatio = int(self.common.doDicEvaluate(data, 'rFRatio'))
            updateDateTime = data['updateDateTime']
            self.assertTrue(int(high) >= int(open) >= int(low))  # 开盘价在最高价最低价之间
            self.assertTrue(int(high) >= int(close) >= int(low))  # 收盘价在最高价最低价之间
            # self.assertTrue(int(high) >= int(average) >= int(low))  # 均价在最高价最低价之间
            if ('{}_{}_last_check_time'.format(code, peroidType) in assert_json.keys()):
                if updateDateTime == assert_json['{}_{}_last_check_time'.format(code, peroidType)]:  # 代表同一根K线上的更新
                    if updateDateTime != assert_json[
                        '{}_{}_first_check_time'.format(code, peroidType)]:     # 校验的第一根K线的话，没有上一跟k线的数据，故此处跳过
                        self.assertTrue(riseFall == close - assert_json['{}_{}_close'.format(code, peroidType)])
                        self.assertTrue(
                            rFRatio == int(10000 * riseFall / (assert_json['{}_{}_close'.format(code, peroidType)])))
                    else:
                        pass
                else:  # 代表K线上的新的更新
                    assert_json['{}_{}_close'.format(code, peroidType)] = assert_json[
                        '{}_{}_float_close'.format(code, peroidType)]
                    self.assertTrue(riseFall == close - assert_json['{}_{}_close'.format(code, peroidType)])
                    self.assertTrue(
                        rFRatio == int(10000 * riseFall / (assert_json['{}_{}_close'.format(code, peroidType)])))
                    assert_json['{}_{}_last_check_time'.format(code, peroidType)] = updateDateTime
            else:  # 某合约、某种类型的K线第一次更新,进行数据初始化
                assert_json['{}_{}_close'.format(code, peroidType)] = close
                assert_json['{}_{}_last_check_time'.format(code, peroidType)] = updateDateTime
                assert_json['{}_{}_first_check_time'.format(code, peroidType)] = updateDateTime
            assert_json['{}_{}_float_close'.format(code, peroidType)] = close  # 保留收盘价，再切换新的K线时候校验

            updateDateTimeStamp = int(time.mktime(time.strptime(updateDateTime, "%Y%m%d%H%M%S"))) * 1000
            if self.is_before_data:
                self.assertTrue(int(updateDateTimeStamp) <= int(self.sub_time))  # 订阅服务时用来判断订阅时间与源时间
                self.assertTrue(int(updateDateTimeStamp) >= int(self.start_time))  # 订阅服务时用来判断APP开始时间与源时间
            # 数据库校验(因需要一直抓取tick，故此处只抽取离最近时间的若干根K线校验,最新一根会实时更新，也不做校验)
            if latest_time_stamp - 1 * 60 * 1000 >= updateDateTimeStamp >= latest_time_stamp - 5 * 60 * 1000:
                start_time_stamp = updateDateTimeStamp - 60 * 1000
                sql_result = self.sq.cal_get_tick(instr_code=code, start_time=start_time_stamp, end_time=updateDateTimeStamp)
                self.assertTrue(high == sql_result['max_price'])
                self.assertTrue(low == sql_result['min_price'])
                self.assertTrue(open == sql_result['open_price'])
                self.assertTrue(close == sql_result['close_price'])
                # self.assertTrue(vol == sql_result['sum_vol'])
                # self.assertTrue(average == sql_result['av_price'])

    def test_07_PushKLineData(self):
        # 推送K线数据
        if self.check_json_list == None:
            check_info = self.sq.get_pub_json_records('60', 1000)
        else:
            check_info = self.check_json_list
        self.assertTrue(check_info.__len__() >= 1)
        self.logger.debug('{} items to check!'.format(check_info.__len__()))
        assert_json = {}
        for info in check_info:
            if self.check_json_list == None:
                record_time = info[1]
                json_info = json.loads(info[0])
            else:
                record_time = int(time.time())  # 因是实时传入，所以可以取当前时间
                json_info = info
            self.logger.debug(json_info)
            if not self.is_before_data:    # 实时push
                exchange = json_info['exchange']
                code = json_info['code']
                kData = json_info['kData']
                peroidType = json_info['peroidType']
                if self.check_json_list == None:
                    get_info = json.loads(check_info[-1][0])
                    latest_time = get_info['kData']['KLineKey']
                else:
                    latest_time = self.common.searchDicKV(check_info[-1], 'KLineKey')
            else:   # app订阅历史数据直接返回data list，不返回exchange、code字段
                exchange = self.exchange
                code = self.instr_code
                kData = json_info
                peroidType = self.peroid_type
                latest_time = self.common.searchDicKV(check_info[-1], 'KLineKey')
            latest_time_stamp = int(time.mktime(time.strptime(latest_time, "%Y%m%d%H%M%S"))) * 1000
            high = int(kData['high'])
            open = int(kData['open'])
            low = int(kData['low'])
            close = int(kData['close'])
            currVol = int(self.common.doDicEvaluate(kData, 'currVol'))
            vol = int(self.common.doDicEvaluate(kData, 'vol'))
            openInterest = int(kData['openInterest'])
            # amount = int(kData['amount']) # bug to be fix
            riseFall = int(self.common.doDicEvaluate(kData, 'riseFall'))
            rFRatio = int(self.common.doDicEvaluate(kData, 'rFRatio'))
            peroidTypeInt = k_type_convert(peroidType)
            exchangeInt = exchange_convert(exchange)
            if peroidTypeInt in [KLinePeriodType.DAY, KLinePeriodType.WEEK, KLinePeriodType.MONTH, KLinePeriodType.SEASON, KLinePeriodType.YEAR]:  # 日K级别及以上类型才有下面字段
                settlementPrice = kData['settlementPrice']
                preSettlement = kData['preSettlement']
                preClose = kData['preClose']
            updateDateTime = kData['updateDateTime']
            KLineKey = kData['KLineKey']

            self.assertTrue(int(high) >= int(open) >= int(low))  # 开盘价在最高价最低价之间
            self.assertTrue(int(high) >= int(close) >= int(low))  # 收盘价在最高价最低价之间
            # self.assertTrue(int(high) >= int(average) >= int(low))  # 均价在最高价最低价之间

            if ('{}_{}_last_check_time'.format(code, peroidType) in assert_json.keys()):
                if KLineKey == assert_json['{}_{}_last_check_time'.format(code, peroidType)]:     # 代表同一根K线上的更新
                    if KLineKey != assert_json['{}_{}_first_check_time'.format(code, peroidType)]:        # 校验的第一根K线的话，没有上一跟k线的数据，故此处跳过
                        self.assertTrue(riseFall == close - assert_json['{}_{}_close'.format(code, peroidType)])
                        self.assertTrue(rFRatio == int(10000 * riseFall / (assert_json['{}_{}_close'.format(code, peroidType)])))
                        self.assertTrue(currVol == vol - assert_json['{}_{}_last_vol'.format(code, peroidType)])
                    else:
                        pass
                else:       # 代表K线上的新的更新
                    self.assertTrue(int(KLineKey) > int(assert_json['{}_{}_last_check_time'.format(code, peroidType)]))
                    assert_json['{}_{}_close'.format(code, peroidType)] = assert_json['{}_{}_float_close'.format(code, peroidType)]
                    assert_json['{}_{}_last_vol'.format(code, peroidType)] = assert_json['{}_{}_float_vol'.format(code, peroidType)]
                    self.assertTrue(riseFall == close - assert_json['{}_{}_close'.format(code, peroidType)])
                    self.assertTrue(rFRatio == int(10000 * riseFall / (assert_json['{}_{}_close'.format(code, peroidType)])))
                    self.assertTrue(currVol == vol - assert_json['{}_{}_last_vol'.format(code, peroidType)])
                    assert_json['{}_{}_last_check_time'.format(code, peroidType)] = KLineKey
            else:       # 某合约、某种类型的K线第一次更新,进行数据初始化
                assert_json['{}_{}_close'.format(code, peroidType)] = close
                assert_json['{}_{}_last_vol'.format(code, peroidType)] = vol
                assert_json['{}_{}_last_check_time'.format(code, peroidType)] = KLineKey
                assert_json['{}_{}_first_check_time'.format(code, peroidType)] = KLineKey
            assert_json['{}_{}_float_close'.format(code, peroidType)] = close       # 保留收盘价，再切换新的K线时候校验
            assert_json['{}_{}_float_vol'.format(code, peroidType)] = vol       # 保留成交量，再切换新的K线时候校验
            if self.is_before_data:
                updateDateTimeStamp = int(time.mktime(time.strptime(updateDateTime, "%Y%m%d%H%M%S"))) * 1000
                self.assertTrue(int(self.start_time) <= int(updateDateTimeStamp) <= int(self.sub_time))  # 订阅服务时用来判断订阅时间与源时间


# --------------------------------------------计算服务end-------------------------------------------------
if __name__ == '__main_':
    unittest.main()
