#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : ddt_excel.py
# @Author: Lizi
# @Date  : 2020/12/1

import openpyxl
import unittest
import ddt


def get_excel_data():
    data_list = []
    excel = openpyxl.load_workbook('./test_ddt.xlsx')
    sheet = excel.active
    # 获取所有行，使用list转换成列表
    rows = list(sheet.rows)
    for row in list(rows[1:len(rows)]):
        test_data = {}
        test_data.setdefault(row[0].value, row[1].value)
        data_list.append(test_data)

    return data_list


@ddt.ddt()
class Test_excel(unittest.TestCase):
    data = get_excel_data()

    @ddt.data(*data)
    # @ddt.unpack
    def test_excel_01(self, username):
        print('用户名为:', username)
        # print('密码为：', pwd)


if __name__ == '__main__':
    unittest.main()
