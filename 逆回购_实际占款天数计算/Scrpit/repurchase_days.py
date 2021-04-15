#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : repurchase_days.py
# @Author: Lizi
# @Date  : 2021/4/14

from Scrpit import calender_list
import datetime
import time
from log_Script.log_demo import logger


class RepurchaseDays():
    def __init__(self):
        self.calendar = calender_list.get_date()
        self.dates_list = self.calendar[0]
        self.trade_type_list = self.calendar[1]

    def get_first_delivery_day(self, t0_trade: str):
        """计算首次交收日"""
        for date in self.dates_list:
            if t0_trade == date:
                num = 0
                for trade_value in self.trade_type_list[self.dates_list.index(date) + 1:]:
                    num += 1
                    if trade_value == 1:
                        logger.info(f"跳过的天数：{num}")
                        self.first_delivery_day = self.dates_list[self.dates_list.index(date) + num]
                        logger.info(f"首期清算日为: {t0_trade}")
                        logger.info(f"首期交收日为: {self.first_delivery_day}")
                        return self.first_delivery_day

    def get_liquidations_day(self, t0_trade: str, repurchase_type: int):
        """计算到期清算日"""
        self.liquidations_day = self.dates_list[self.dates_list.index(t0_trade) + repurchase_type]
        num = 0
        if self.trade_type_list[self.dates_list.index(self.liquidations_day)] != 1:
            for trade_value in self.trade_type_list[self.dates_list.index(self.liquidations_day) + 1:]:
                num += 1
                if trade_value == 1:
                    logger.info(f"遇到非交易日跳过的天数：{num}")
                    self.liquidations_day = self.dates_list[self.dates_list.index(t0_trade) + repurchase_type + num]
                    break
        logger.info(f"到期清算日：{self.liquidations_day}")
        return self.liquidations_day

    def get_due_delivery_day(self):
        """计算到期交收日"""
        num = 0
        for trade_value in self.trade_type_list[self.dates_list.index(self.liquidations_day) + 1:]:
            num += 1
            if trade_value == 1:
                logger.info(f"遇到非交易日跳过的天数：{num}")
                self.due_delivery_day = self.dates_list[self.dates_list.index(self.liquidations_day) + num]
                logger.info(f"到期交收日为：{self.due_delivery_day}")
                return self.due_delivery_day

    def cal_num_days(self):
        """计算实际占款天数"""
        time_1 = time.strptime(self.first_delivery_day, "%Y/%m/%d")
        time_2 = time.strptime(self.due_delivery_day, "%Y/%m/%d")
        T0_trade_datetime = datetime.datetime(time_1[0], time_1[1], time_1[2])
        due_delivery_datetime = datetime.datetime(time_2[0], time_2[1], time_2[2])
        logger.info(f"实际占款天数：{due_delivery_datetime - T0_trade_datetime}")


if __name__ == '__main__':
    repurchase_day = RepurchaseDays()
    repurchase_day.get_first_delivery_day('2021/04/14')
    repurchase_day.get_liquidations_day('2021/04/14', 182)
    repurchase_day.get_due_delivery_day()
    repurchase_day.cal_num_days()
