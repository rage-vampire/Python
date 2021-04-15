#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : modified.py
# @Author: Lizi
# @Date  : 2020/10/19

import sqlite3

conn = sqlite3.connect('./test.db')
cur = conn.cursor()

sql = 'update t_person set age = ? where name=?'

try:
    cur.execute(sql, ('01', '张三'))
    conn.commit()
except Exception as e:
    print(e)
    print('修改失败')
    conn.rollback()
finally:
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()

