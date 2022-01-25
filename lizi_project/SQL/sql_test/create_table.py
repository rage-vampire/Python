#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : create_table.py
# @Author: Lizi
# @Date  : 2020/10/19
import sqlite3

# 硬盘上创建连接，connect打开或创建一数据库，没有则创建新的
conn = sqlite3.connect('./test.db')
# 获取游标
cur = conn.cursor()

# 执行游标
sql = 'create table t_person (pno INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(30) NOT NULL, age INTEGER)'
try:
    conn.execute(sql)
except Exception as e:
    print(e)
    print('创建表失败')
finally:
    cur.close()
    conn.close()