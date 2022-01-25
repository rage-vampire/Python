# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/6/20
# @Software: PyCharm

from py_redis.base import RedisDb
from pb_files.quote_type_def_pb2 import *
from pb_files.quote_msg_def_pb2 import *
from google.protobuf import json_format
import json


class MarketRedisDBClient(RedisDb):
    def get_trade_data(self, exchange_int, instr_code, start_time_stamp, end_time_stamp):
        key = '{}_{}'.format(exchange_int, instr_code)
        value_list = self.GetZsetValueByScore(key, start_time_stamp, end_time_stamp)
        json_rsp_list = []
        for value in value_list:
            single_data = TradeTick()
            single_data.ParseFromString(value)
            json_single_data = json_format.MessageToJson(single_data)
            json_single_data = json.loads(json_single_data)
            json_rsp_list.append(json_single_data)
        return json_rsp_list

    def get_minute_interval(self, kline_timestamp):
        return [int(kline_timestamp - 1000 * 60), int(kline_timestamp - 1)]


if __name__ == '__main__':
    madb = MarketRedisDBClient()
    aaa = madb.get_trade_data(16, 'HHI2007', 1591596141774, 1591596564119)
    print(1)