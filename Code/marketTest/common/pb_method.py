# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/6/22
# @Software: PyCharm


from pb_files.quote_type_def_pb2 import *
from pb_files.common_type_def_pb2 import *
from common.test_log.ed_log import get_log

logger = get_log()


def k_type_convert(input_str):
    if isinstance(input_str, int):
        return input_str
    elif input_str == 'MINUTE':
        return KLinePeriodType.MINUTE
    elif input_str == 'THREE_MIN':
        return KLinePeriodType.THREE_MIN
    elif input_str == 'FIVE_MIN':
        return KLinePeriodType.FIVE_MIN
    elif input_str == 'FIFTEEN_MIN':
        return KLinePeriodType.FIFTEEN_MIN
    elif input_str == 'THIRTY_MIN':
        return KLinePeriodType.THIRTY_MIN
    elif input_str == 'HOUR':
        return KLinePeriodType.HOUR
    elif input_str == 'TWO_HOUR':
        return KLinePeriodType.TWO_HOUR
    elif input_str == 'FOUR_HOUR':
        return KLinePeriodType.FOUR_HOUR
    elif input_str == 'DAY':
        return KLinePeriodType.DAY
    elif input_str == 'WEEK':
        return KLinePeriodType.WEEK
    elif input_str == 'MONTH':
        return KLinePeriodType.MONTH
    else:
        logger.debug('Error klinePeriodType: {}'.format(input_str))


def exchange_convert(input_str):
    if input_str == 'HKFE':
        return ExchangeType.HKFE
    elif input_str == 'NYMEX':
        return KLinePeriodType.NYMEX
    elif input_str == 'COMEX':
        return KLinePeriodType.COMEX
    elif input_str == 'ASE':
        return KLinePeriodType.ASE
    elif input_str == 'ASX':
        return KLinePeriodType.ASX
    elif input_str == 'CBOE':
        return KLinePeriodType.CBOE
    else:
        logger.debug('Error exchange: {}'.format(input_str))