# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/6/16
# @Software: PyCharm

from google.protobuf import json_format
from pb_files.quote_msg_def_pb2 import *
from pb_files.quote_type_def_pb2 import *
from pb_files.common_type_def_pb2 import *
from py_rocksdb.base import RocksDBClient
from common.common_method import Common
from test_config import *
import json
import time
import calendar
import datetime
import arrow


class MarketRocksDBClient(RocksDBClient):
    def get_single_value(self, key):
        json_single_data = None
        binary_info = self.get(key)
        if binary_info != None:
            if 'KLINE_' in key:
                recv_data = KlineData()
                recv_data.ParseFromString(binary_info)
                json_single_data = json_format.MessageToJson(recv_data)
                json_single_data = json.loads(json_single_data)
            elif 'KLINEMIN_' in key:
                recv_data = KlineDataMin()
                recv_data.ParseFromString(binary_info)
                json_single_data = json_format.MessageToJson(recv_data)
                json_single_data = json.loads(json_single_data)
            elif 'TRADETICK_' in key:
                recv_data = TradeTick()
                recv_data.ParseFromString(binary_info)
                json_single_data = json_format.MessageToJson(recv_data)
                json_single_data = json.loads(json_single_data)
            else:
                self.logger('Key error, please check! key: {}'.format(key))
        else:
            pass
        return json_single_data

    def get_multi_value(self, key_list):
        value_list = []
        for key in key_list:
            value = self.get_single_value(key)
            if value != None:
                value_list.append(value)
        return value_list


class DBMethod(object):
    def __init__(self):
        self.common = Common()
        self.logger = self.common.logger

    def get_recent_stamp_list(self, peroid_type_int, exchange_int):
        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime(int(time.time())))
        time_str_list = []
        recent_time_stamp_list = []
        if exchange_int == ExchangeType.HKFE:
            if peroid_type_int == KLinePeriodType.THREE_MIN:
                time_str_prefix = time_str[:-6]
                # 暂时只校验白天的
                for hour_str in ['09', '10', '11', '12', '13', '14', '15', '16']:
                    time_str_fix = time_str_prefix + hour_str
                    if hour_str not in ['09', '12', '13', '16']:
                        for min_str in range(0, 60, 3):
                            min_str = self.common.fixIntNum(min_str, 2)
                            time_str_fix = time_str_fix + str(min_str) + '00'
                            if int(time_str_fix) < int(time_str):
                                time_str_list.append(time_str_fix)
                                time_str_fix = time_str_prefix + hour_str
                            else:
                                break
                    elif hour_str == '09':
                        for min_str in range(18, 60, 3):
                            min_str = self.common.fixIntNum(min_str, 2)
                            time_str_fix = time_str_fix + str(min_str) + '00'
                            if int(time_str_fix) < int(time_str):
                                time_str_list.append(time_str_fix)
                                time_str_fix = time_str_prefix + hour_str
                            else:
                                break
                    elif hour_str == '12':
                        min_str = '00'
                        time_str_fix = time_str_fix + str(min_str) + '00'
                        if int(time_str_fix) < int(time_str):
                            time_str_list.append(time_str_fix)
                    elif hour_str == '13':
                        for min_str in range(3, 60, 3):
                            min_str = self.common.fixIntNum(min_str, 2)
                            time_str_fix = time_str_fix + str(min_str) + '00'
                            if int(time_str_fix) < int(time_str):
                                time_str_list.append(time_str_fix)
                                time_str_fix = time_str_prefix + hour_str
                            else:
                                break
                    elif hour_str == '16':
                        for min_str in range(0, 33, 3):
                            min_str = self.common.fixIntNum(min_str, 2)
                            time_str_fix = time_str_fix + str(min_str) + '00'
                            if int(time_str_fix) < int(time_str):
                                time_str_list.append(time_str_fix)
                                time_str_fix = time_str_prefix + hour_str
                            else:
                                break

            elif peroid_type_int == KLinePeriodType.FIVE_MIN:
                time_str_prefix = time_str[:-6]
                # 暂时只校验白天的
                for hour_str in ['09', '10', '11', '12', '13', '14', '15', '16']:
                    time_str_fix = time_str_prefix + hour_str
                    if hour_str not in ['09', '12', '13', '16']:
                        for min_str in range(0, 60, 5):
                            min_str = self.common.fixIntNum(min_str, 2)
                            time_str_fix = time_str_fix + str(min_str) + '00'
                            if int(time_str_fix) < int(time_str):
                                time_str_list.append(time_str_fix)
                                time_str_fix = time_str_prefix + hour_str
                            else:
                                break
                    elif hour_str == '09':
                        for min_str in range(20, 60, 5):
                            min_str = self.common.fixIntNum(min_str, 2)
                            time_str_fix = time_str_fix + str(min_str) + '00'
                            if int(time_str_fix) < int(time_str):
                                time_str_list.append(time_str_fix)
                                time_str_fix = time_str_prefix + hour_str
                            else:
                                break
                    elif hour_str == '12':
                        min_str = '00'
                        time_str_fix = time_str_fix + str(min_str) + '00'
                        if int(time_str_fix) < int(time_str):
                            time_str_list.append(time_str_fix)
                    elif hour_str == '13':
                        for min_str in range(5, 60, 5):
                            min_str = self.common.fixIntNum(min_str, 2)
                            time_str_fix = time_str_fix + str(min_str) + '00'
                            if int(time_str_fix) < int(time_str):
                                time_str_list.append(time_str_fix)
                                time_str_fix = time_str_prefix + hour_str
                            else:
                                break
                    elif hour_str == '16':
                        for min_str in range(0, 35, 5):
                            min_str = self.common.fixIntNum(min_str, 2)
                            time_str_fix = time_str_fix + str(min_str) + '00'
                            if int(time_str_fix) < int(time_str):
                                time_str_list.append(time_str_fix)
                                time_str_fix = time_str_prefix + hour_str
                            else:
                                break

            elif peroid_type_int == KLinePeriodType.FIFTEEN_MIN:
                time_str_prefix = time_str[:-6]
                # 暂时只校验白天的
                for hour_str in ['09', '10', '11', '12', '13', '14', '15', '16']:
                    time_str_fix = time_str_prefix + hour_str
                    if hour_str not in ['09', '12', '13', '16']:
                        for min_str in range(0, 60, 15):
                            min_str = self.common.fixIntNum(min_str, 2)
                            time_str_fix = time_str_fix + str(min_str) + '00'
                            if int(time_str_fix) < int(time_str):
                                time_str_list.append(time_str_fix)
                                time_str_fix = time_str_prefix + hour_str
                            else:
                                break
                    elif hour_str == '09':
                        for min_str in range(30, 60, 15):
                            min_str = self.common.fixIntNum(min_str, 2)
                            time_str_fix = time_str_fix + str(min_str) + '00'
                            if int(time_str_fix) < int(time_str):
                                time_str_list.append(time_str_fix)
                                time_str_fix = time_str_prefix + hour_str
                            else:
                                break
                    elif hour_str == '12':
                        min_str = '00'
                        time_str_fix = time_str_fix + str(min_str) + '00'
                        if int(time_str_fix) < int(time_str):
                            time_str_list.append(time_str_fix)
                    elif hour_str == '13':
                        for min_str in range(15, 60, 15):
                            min_str = self.common.fixIntNum(min_str, 2)
                            time_str_fix = time_str_fix + str(min_str) + '00'
                            if int(time_str_fix) < int(time_str):
                                time_str_list.append(time_str_fix)
                                time_str_fix = time_str_prefix + hour_str
                            else:
                                break
                    elif hour_str == '16':
                        for min_str in range(0, 45, 15):
                            min_str = self.common.fixIntNum(min_str, 2)
                            time_str_fix = time_str_fix + str(min_str) + '00'
                            if int(time_str_fix) < int(time_str):
                                time_str_list.append(time_str_fix)
                                time_str_fix = time_str_prefix + hour_str
                            else:
                                break

            elif peroid_type_int == KLinePeriodType.THIRTY_MIN:
                time_str_prefix = time_str[:-6]
                # 暂时只校验白天的
                for hour_str in ['09', '10', '11', '12', '13', '14', '15', '16']:
                    time_str_fix = time_str_prefix + hour_str
                    if hour_str not in ['09', '12', '13', '16']:
                        for min_str in range(0, 60, 30):
                            min_str = self.common.fixIntNum(min_str, 2)
                            time_str_fix = time_str_fix + str(min_str) + '00'
                            if int(time_str_fix) < int(time_str):
                                time_str_list.append(time_str_fix)
                                time_str_fix = time_str_prefix + hour_str
                            else:
                                break
                    elif hour_str == '09':
                        pass    # 9点区间的半小时K只有9.30这一根，区间属于 0245-0300、0915-0930之和,跨区间，此处不便校验，先跳过
                    elif hour_str == '12':
                        min_str = '00'
                        time_str_fix = time_str_fix + str(min_str) + '00'
                        if int(time_str_fix) < int(time_str):
                            time_str_list.append(time_str_fix)
                    elif hour_str == '13':
                        for min_str in range(30, 60, 30):
                            min_str = self.common.fixIntNum(min_str, 2)
                            time_str_fix = time_str_fix + str(min_str) + '00'
                            if int(time_str_fix) < int(time_str):
                                time_str_list.append(time_str_fix)
                                time_str_fix = time_str_prefix + hour_str
                            else:
                                break
                    elif hour_str == '16':
                        for min_str in range(0, 60, 30):
                            min_str = self.common.fixIntNum(min_str, 2)
                            time_str_fix = time_str_fix + str(min_str) + '00'
                            if int(time_str_fix) < int(time_str):
                                time_str_list.append(time_str_fix)
                                time_str_fix = time_str_prefix + hour_str
                            else:
                                break

            elif peroid_type_int == KLinePeriodType.HOUR:
                time_str_prefix = time_str[:-6]
                # 暂时只校验白天的
                # 9点区间的1小时K只有9.30这一根，区间属于 0215-0300、0915-0930之和,跨区间，此处不便校验，先跳过; 13.30同理
                for hour_str in ['10', '11', '14', '15', '16']:
                    time_str_fix = time_str_prefix + hour_str
                    min_str = '30'
                    time_str_fix = time_str_fix + str(min_str) + '00'
                    if int(time_str_fix) < int(time_str):
                        time_str_list.append(time_str_fix)
                    else:
                        break

            elif peroid_type_int == KLinePeriodType.TWO_HOUR:
                time_str_prefix = time_str[:-6]
                # 暂时只校验白天的
                # 14.30这一根，区间属于 1130-1200、1300-1430之和,跨区间，此处不便校验，先跳过
                for hour_str in ['11', '16']:
                    time_str_fix = time_str_prefix + hour_str
                    min_str = '30'
                    time_str_fix = time_str_fix + str(min_str) + '00'
                    if int(time_str_fix) < int(time_str):
                        time_str_list.append(time_str_fix)
                    else:
                        break

            elif peroid_type_int == KLinePeriodType.FOUR_HOUR:
                # 4小时K连续的k线区间只有1715-2115和2115-0115两个区间，校验这两个区间
                today = datetime.date.today()
                today_info1 = datetime.datetime(today.year, today.month, today.day, 21, 15, 0)
                last_day = today_info1 - datetime.timedelta(days=1)
                recent_time_stamp1 = int(time.mktime(time.strptime(str(last_day), '%Y-%m-%d %H:%M:%S')))
                recent_time_stamp_list.append(recent_time_stamp1)
                today_info2 = datetime.datetime(today.year, today.month, today.day, 1, 15, 0)
                recent_time_stamp2 = int(time.mktime(time.strptime(str(today_info2), '%Y-%m-%d %H:%M:%S')))
                recent_time_stamp_list.append(recent_time_stamp2)
                return recent_time_stamp_list

            elif peroid_type_int == KLinePeriodType.DAY:
                get_num = 3     # 暂时只返回校验过去的三天
                today = datetime.date.today()
                today_info = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
                last_day = today_info
                for _ in range(get_num):
                    last_day = last_day - datetime.timedelta(days=1)
                    recent_time_stamp = int(time.mktime(time.strptime(str(last_day), '%Y-%m-%d %H:%M:%S')))
                    recent_time_stamp_list.append(recent_time_stamp)
                return recent_time_stamp_list

            elif peroid_type_int == KLinePeriodType.WEEK:
                get_num = 3  # 暂时只返回校验过去的三周
                test_day = time.localtime()
                today_wday = test_day.tm_wday   # [0,1,2,3,4,5,6]代表周一到周日
                today = datetime.date.today()
                today_info = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
                this_monday = today_info - datetime.timedelta(days=today_wday)
                last_monday = this_monday
                for _ in range(get_num):
                    last_monday = last_monday - datetime.timedelta(days=7)
                    recent_time_stamp = int(time.mktime(time.strptime(str(last_monday), '%Y-%m-%d %H:%M:%S')))
                    recent_time_stamp_list.append(recent_time_stamp)
                return recent_time_stamp_list

            elif peroid_type_int == KLinePeriodType.MONTH:
                get_num = 1  # 暂时只返回校验过去的三月
                now = arrow.now()
                for _ in range(get_num):
                    last_month_str = now.shift(months=-1).format('YYYYMM')
                    recent_time_stamp = int(time.mktime(time.strptime(str(last_month_str), '%Y%m')))
                    recent_time_stamp_list.append(recent_time_stamp)
                    now = now.shift(months=-1)
                return recent_time_stamp_list

        recent_time_stamp_list = [int(time.mktime(time.strptime(time_str, "%Y%m%d%H%M%S"))) for time_str in time_str_list]
        recent_time_stamp_list = sorted(recent_time_stamp_list)
        return recent_time_stamp_list

    def get_minute_keys(self, instr_code, exchange, peroid_type, kline_key_stamp):
        # 传入K线的相关信息，输出对应的分时线的key值(此方法要求区间连续)
        minutes_num = 0
        min_time_stamp_list = []
        if peroid_type == KLinePeriodType.MINUTE:
            minutes_num = 1
        elif peroid_type == KLinePeriodType.THREE_MIN:
            minutes_num = 3
        elif peroid_type == KLinePeriodType.FIVE_MIN:
            minutes_num = 5
        elif peroid_type == KLinePeriodType.FIFTEEN_MIN:
            minutes_num = 15
        elif peroid_type == KLinePeriodType.THIRTY_MIN:
            minutes_num = 30
        elif peroid_type == KLinePeriodType.HOUR:
            minutes_num = 60
        elif peroid_type == KLinePeriodType.TWO_HOUR:
            minutes_num = 60 * 2
        elif peroid_type == KLinePeriodType.FOUR_HOUR:
            minutes_num = 60 * 4
        elif peroid_type == KLinePeriodType.DAY:
            minutes_num = 60 * 24
        elif peroid_type == KLinePeriodType.WEEK:
            minutes_num = 60 * 24 * 7
        elif peroid_type == KLinePeriodType.MONTH:
            time_struct = time.localtime(kline_key_stamp)
            month_contain_days = calendar.monthrange(time_struct.tm_year, time_struct.tm_mon)[1]
            minutes_num = 60 * 24 * month_contain_days

        if peroid_type not in [KLinePeriodType.DAY, KLinePeriodType.WEEK, KLinePeriodType.MONTH]:
            min_time_stamp_list = reversed([(kline_key_stamp - i * 60) for i in range(minutes_num)])
        elif peroid_type == KLinePeriodType.DAY:
            if exchange == ExchangeType.HKFE:
                # 港期每日开盘时间是夜市开始时间，下午5.15
                min_time_stamp_list = reversed([(kline_key_stamp + 17 * 60 * 60 + 15 * 60 - i * 60) for i in range(minutes_num)])
        elif peroid_type == KLinePeriodType.WEEK:
            if exchange == ExchangeType.HKFE:
                # 港期每周开盘时间是周五夜市开始时间，下午5.15
                min_time_stamp_list = reversed(
                    [(kline_key_stamp + 4 * 24 * 60 * 60 + 17 * 60 * 60 + 15 * 60 - i * 60) for i in range(minutes_num)])
        elif peroid_type == KLinePeriodType.MONTH:
            if exchange == ExchangeType.HKFE:
                # 港期每日开盘时间是夜市开始时间，下午5.15
                min_time_stamp_list = [(kline_key_stamp - (6 * 60 * 60 + 45 * 60) + i * 60) for i in
                     range(1, minutes_num + 1)]
        else:
            self.logger.debug('Error peroid_type: {}'.format(peroid_type))
        key_list = [
            ('KLINEMIN_{}_{}_{}'.format(exchange, instr_code, time.strftime("%Y%m%d%H%M%S", time.localtime(j)))) for
            j in min_time_stamp_list]
        return key_list

    def get_minute_keys_by_time(self, instr_code, exchange, start_time_stamp, end_time_stamp):
        # 传入开始及结束对应的时间戳，则把对应区间的key值返回
        key_list = [
            ('KLINEMIN_{}_{}_{}'.format(exchange, instr_code, time.strftime("%Y%m%d%H%M%S", time.localtime(time_stamp)))) for
            time_stamp in range(start_time_stamp + 60, end_time_stamp + 60, 60)]
        return key_list

    def get_recent_interval_list(self, peroid_type_int, exchange_int):
        # 此方法用于校验跨区间的K线的情况
        interval_list = []
        if exchange_int == ExchangeType.HKFE:
            if peroid_type_int == KLinePeriodType.THIRTY_MIN:
                # 半小时K只有9.30这一根，区间属于 0245-0300、0915-0930之和,跨区间
                today = datetime.date.today()
                end_info = datetime.datetime(today.year, today.month, today.day, 9, 30, 0)
                end_info_time_stamp = int(time.mktime(time.strptime(str(end_info), '%Y-%m-%d %H:%M:%S')))
                if time.localtime().tm_wday != 0:   # 非周一
                    start_info = end_info - datetime.timedelta(hours=6, minutes=45)
                else:
                    start_info = end_info - datetime.timedelta(days=2, hours=6, minutes=45)
                start_info_time_stamp = int(time.mktime(time.strptime(str(start_info), '%Y-%m-%d %H:%M:%S')))
                if end_info_time_stamp < time.time():
                    interval_list.append([start_info_time_stamp, end_info_time_stamp])

            elif peroid_type_int == KLinePeriodType.HOUR:
                # 9.30这一根，区间属于 0215-0300、0915-0930之和,跨区间;
                today = datetime.date.today()
                end_info = datetime.datetime(today.year, today.month, today.day, 9, 30, 0)
                end_info_time_stamp = int(time.mktime(time.strptime(str(end_info), '%Y-%m-%d %H:%M:%S')))
                if time.localtime().tm_wday != 0:   # 非周一
                    start_info = end_info - datetime.timedelta(hours=7, minutes=15)
                else:
                    start_info = end_info - datetime.timedelta(days=2, hours=7, minutes=15)
                start_info_time_stamp = int(time.mktime(time.strptime(str(start_info), '%Y-%m-%d %H:%M:%S')))
                if end_info_time_stamp < time.time():
                    interval_list.append([start_info_time_stamp, end_info_time_stamp])
                #  13.30
                end_info2 = datetime.datetime(today.year, today.month, today.day, 13, 30, 0)
                end_info_time_stamp2 = int(time.mktime(time.strptime(str(end_info2), '%Y-%m-%d %H:%M:%S')))
                start_info2 = datetime.datetime(today.year, today.month, today.day, 11, 30, 0)
                start_info_time_stamp2 = int(time.mktime(time.strptime(str(start_info2), '%Y-%m-%d %H:%M:%S')))
                if end_info_time_stamp2 < time.time():
                    interval_list.append([start_info_time_stamp2, end_info_time_stamp2])

            elif peroid_type_int == KLinePeriodType.TWO_HOUR:
                # 14.30这一根，区间属于 1130-1200、1300-1430之和,跨区间
                today = datetime.date.today()
                end_info = datetime.datetime(today.year, today.month, today.day, 14, 30, 0)
                end_info_time_stamp = int(time.mktime(time.strptime(str(end_info), '%Y-%m-%d %H:%M:%S')))
                start_info = datetime.datetime(today.year, today.month, today.day, 11, 30, 0)
                start_info_time_stamp = int(time.mktime(time.strptime(str(start_info), '%Y-%m-%d %H:%M:%S')))
                if end_info_time_stamp < time.time():
                    interval_list.append([start_info_time_stamp, end_info_time_stamp])

                # 0930: 0115-0300 , 0915-0930
                end_info2 = datetime.datetime(today.year, today.month, today.day, 9, 30, 0)
                end_info_time_stamp2 = int(time.mktime(time.strptime(str(end_info2), '%Y-%m-%d %H:%M:%S')))
                if time.localtime().tm_wday != 0:  # 非周一
                    start_info2 = end_info2 - datetime.timedelta(hours=8, minutes=15)
                else:
                    start_info2 = end_info2 - datetime.timedelta(days=2, hours=8, minutes=15)
                start_info_time_stamp2 = int(time.mktime(time.strptime(str(start_info2), '%Y-%m-%d %H:%M:%S')))
                if end_info_time_stamp2 < time.time():
                    interval_list.append([start_info_time_stamp2, end_info_time_stamp2])

            elif peroid_type_int == KLinePeriodType.FOUR_HOUR:
                # 11.30这一根，区间属于 0115-0300、0915-1130,跨区间;
                today = datetime.date.today()
                end_info = datetime.datetime(today.year, today.month, today.day, 11, 30, 0)
                end_info_time_stamp = int(time.mktime(time.strptime(str(end_info), '%Y-%m-%d %H:%M:%S')))
                if time.localtime().tm_wday != 0:  # 非周一
                    start_info = end_info - datetime.timedelta(hours=10, minutes=15)
                else:
                    start_info = end_info - datetime.timedelta(days=2, hours=10, minutes=15)
                start_info_time_stamp = int(time.mktime(time.strptime(str(start_info), '%Y-%m-%d %H:%M:%S')))
                if end_info_time_stamp < time.time():
                    interval_list.append([start_info_time_stamp, end_info_time_stamp])
                # 16.30这一根，区间属于 1130-1200、1300-1630之和,跨区间;
                end_info2 = datetime.datetime(today.year, today.month, today.day, 16, 30, 0)
                end_info_time_stamp2 = int(time.mktime(time.strptime(str(end_info2), '%Y-%m-%d %H:%M:%S')))
                start_info2 = datetime.datetime(today.year, today.month, today.day, 11, 30, 0)
                start_info_time_stamp2 = int(time.mktime(time.strptime(str(start_info2), '%Y-%m-%d %H:%M:%S')))
                if end_info_time_stamp2 < time.time():
                    interval_list.append([start_info_time_stamp2, end_info_time_stamp2])
            else:
                self.logger.debug('ktype error: {}'.format(peroid_type_int))
        return interval_list


if __name__ == '__main__':
    db = MarketRocksDBClient(rocksdb_path)
    db_method = DBMethod()
    common = Common()
    # key_list = ['KLINE_16_HHI2006_10_20200615160000', 'KLINEMIN_16_HHI2006_20200615160000', 'KLINEMIN_16_HHI2007_20200617112900']
    # time_start = 20200619011600
    # time_end = 20200619113100
    #
    #
    #
    # key_list = ['KLINEMIN_16_MHI2006_{}'.format(time_str) for time_str in range(time_start, time_end, 1)]
    # minute_info_list = db.get_multi_value(key_list)
    #
    # minute_open = int(minute_info_list[0]['open'])
    # minute_close = int(minute_info_list[-1]['close'])
    # minute_high = max([int(minute_info['high']) for minute_info in minute_info_list])
    # minute_low = min([int(minute_info['low']) for minute_info in minute_info_list])
    # minute_vol = sum([int(common.doDicEvaluate(minute_info, 'vol')) for minute_info in minute_info_list])
    #
    # print(db_method.get_minute_keys('HHI2006', 16, 10, 1592366136000))

    aaa = db_method.get_recent_interval_list(17, 16)
