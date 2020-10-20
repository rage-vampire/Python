#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : sql_connect.py
# @Author: Lizi
# @Date  : 2020/10/20

import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', passwd='123456')
print(conn)
cur = conn.cursor()

# 创建数据库
sql = 'create database my_test'
try:
    cur.execute(sql)
except Exception as e:
    print(e)
    print('创建库失败！')



