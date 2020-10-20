#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : create_table.py
# @Author: Lizi
# @Date  : 2020/10/20
import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', passwd='123456')
print(conn)
cur = conn.cursor()

# 创建表
sql = 'create table sites  (name VARCHAR(255), url VARCHAR(255))'
set_key = "ALTER TABLE sites ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY"
cur.execute(sql)
cur.execute(set_key)