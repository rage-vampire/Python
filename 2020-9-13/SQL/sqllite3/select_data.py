#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : select_data.py
# @Author: Lizi
# @Date  : 2020/10/19

import sqlite3

conn = sqlite3.connect('./test.db')
cur = conn.cursor()

sql = 'select * from t_person'

try:
    cur.execute(sql)
    # cur.fetchall()游标对象查询所有数据，cur.fetchone()游标对象查询一条数据，
    person_all = cur.fetchall()
    for p in person_all:
        print(p)
    # person_one = cur.fetchone()
    # print(person_one)
except Exception as e:
    print(e)
    print('查询失败')

finally:
    cur.close()
    conn.close()
