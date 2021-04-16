#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : writer_csv.py
# @Author: Lizi
# @Date  : 2021/4/15

import csv


"""
writerow:一行行的写入
writerows:一次性写入多行
"""
# with open('./demo.csv','w') as csvfile:
#     writer_file = csv.writer(csvfile)
#     writer_file.writerow(["yanglili"]*5)     # 在第一行写入5个值
#     writer_file.writerows([["yanglili"]*4, ['hauhua']*3])         # 写入两行数据


"""写入带有字段名称的CSV文件"""

with open('demo.csv', 'w', newline='') as csvfile:     # newline=''去除空白行
    filenams = ['first_name', "last_name", 'sex']  # 定义列头
    file = csv.DictWriter(csvfile, fieldnames=filenams, restval="women")
    file.writeheader()   # 写入列头
    file.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    file.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})