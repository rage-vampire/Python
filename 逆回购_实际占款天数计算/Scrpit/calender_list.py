#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : calender_list.py
# @Author: Lizi
# @Date  : 2021/4/13

import xlrd
import pprint
import datetime
import time


def get_date():
    dates = []
    trade_type = []
    excel = xlrd.open_workbook(filename='../trade_datas.xlsx')
    sheet = excel.sheet_by_name('cal')

    col_1 = sheet.col_values(0)
    col_2 = sheet.col_values(1)
    # 获取日期列的数据
    for col_date in range(len(col_1)):
        if sheet.cell(col_date, 0).ctype == 3:
            cell_date = xlrd.xldate_as_tuple(sheet.cell(col_date, 0).value, 0)
            date_time = datetime.datetime(*cell_date)
            strf_date = date_time.strftime('%Y/%m/%d')
            dates.append(strf_date)

    # 获取交易日的类型，1代表交易日，0代表非交易日
    for col_type in range(len(col_2)):
        val = sheet.cell(col_type, 1).value
        trade_type.append(int(val))
    # dates_dict = dict(zip(dates, trade_type))
    return dates, trade_type


if __name__ == '__main__':
    date_list = get_date()
    print(date_list[0])
    print(date_list[1])
