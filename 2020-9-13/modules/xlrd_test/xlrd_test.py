#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : xlrd_test.py
# @Author: Lizi
# @Date  : 2020/11/11

import xlrd

'''xlrd: 对xls、xlsx、xlsm文件进行读操作–读操作效率较高，推荐

    步骤：
        1、获取工作部对象：excel1 = xlrd.open_workbook(filename)
        2、获取sheet表：sheet1 = excel1.sheet_by_name('sheet')或者sheet1 = excel1.sheet_by_index(0)

'''

'''获取工作簿对象'''
excel1 = xlrd.open_workbook(filename='test.xls')

'''获取工作簿中所有sheet的名称，返回一个列表对象，该对象支持索引取值，从0开始'''
# sheet_name = excel1.sheet_names()
# print(sheet_name)

'''获取sheet对象'''
sheet = excel1.sheet_by_name('userinfo')

'''获取所有行、所有列'''
# print(sheet.nrows)
# print(sheet.ncols)

'''获取整行、整列的数据。行和列的索引从0开始'''
# print(sheet.row_values(0))   # 获取第一行的数据
# print(sheet.col_values(0))   # 获取第一列的数据


'''读取某个单元格的数据'''
# print(sheet.cell(0, 0).value)   # 读取A1单元格的数据
# print(sheet.cell(0, 1).value)   # 读取B1单元格的数据

'''读取某行所有单元格的数据   (0,0) (0,1) (0,2)'''
row = sheet.row_values(0)
for i in range(len(row)):
    print(sheet.cell(0, i).value, end=' ')


''' 读取文件中所有单元格的数据
    (0,0) (0,1) (0,2)
    (1,0) (1,1) (1,2)
    (2,0) (2,1) (2,2)'''
row = sheet.row_values(0)
col = sheet.col_values(0)
for i in range(len(row)):
    for j in range(len(col)):
        print(sheet.cell(i, j).value, end=' ')
    print(' ')




