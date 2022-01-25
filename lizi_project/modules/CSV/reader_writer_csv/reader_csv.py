#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : reader_csv.py
# @Author: Lizi
# @Date  : 2021/4/15

import csv

"""读文件"""
# with open('./trade_datas.csv', 'r') as f:
#     reader = csv.reader(f)    # reader是一个可迭代的list对象，CSV中的一行就是一个list
#     for row in reader:
#         print(row)      # 遍历reader中的所有行，按行输出
#         print(row[0])   # 输出第一列


# """获取文件的第一行"""
# with open('./trade_datas.csv', 'r') as f:
#     reader = csv.reader(f)    # reader是一个可迭代的list对象，CSV中的一行就是一个list
#     header_row = next(reader)    # next(),迭代器的方法，读取第一行
#     print(header_row)


"""获取文件的头及其索引值"""
with open('trade_datas.csv', 'r') as f:
    reader = csv.reader(f)    # reader是一个可迭代的list对象，CSV中的一行就是一个list
    header_row = next(reader)    # next(),迭代器的方法，读取第一行
    for index, value in enumerate(header_row):
        print(index, value)


"""
读取带有字段名称的CSV文件
fieldnames：字段名称，默认是第一行的数据。
restkey：当实际的字段数量大于上面参数指定的数量时，多出来的字段名称就是这个restkey指定。
restval: 与上面相反，当实际的字段数量少的时候，多余的字段名称的值就由restval指定。
其他基本和reader一致。
"""
with open('./trade_datas.csv', 'r') as f:
    reader = csv.DictReader(f, fieldnames='AB')
    for row in reader:
        print(row)
