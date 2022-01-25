#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : xlwt_test.py
# @Author: Lizi
# @Date  : 2020/11/11

import xlwt

""" xlwt: 对xls文件进行写操作–写操作效率较高，但是不能执行xlsx文件
    步骤：
        1、新建一个工作簿 excel = xlwt.Workbook()；
        2、在工作簿中添加sheet页 sheet = excel.add_sheet('str')
        3、写入数据 ;
        4、保存工作簿"""


'''建立一个工作簿'''
excel = xlwt.Workbook()


'''添加一个sheet表格'''
sheet = excel.add_sheet('userinfo')


'''写入数据
    支持索引，行和列都是从0开始'''
sheet.write(0, 0,' username')    # 在A1单元格写入数据
sheet.write(0, 1, 'passwd')    # 在B1单元格写入数据
excel.save('test.xls')


'''同时写入一行数据'''
row_list = ['lizi', 123456]
for i in range(len(row_list)):
    sheet.write(1,i,row_list[i])
excel.save('test.xls')