#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : insert_into.py
# @Author: Lizi
# @Date  : 2020/10/19

import sqlite3
conn = sqlite3.connect('./test.db')
cur = conn.cursor()

'''# 向表中插入一条数据cur.execute()'''
sql = 'insert into t_person (name,age) values (?,?)'
try:
    # 执行sql语句
    cur.execute(sql,('张三', 24))
    # 提交事务
    conn.commit()
    print('插入成功')
except Exception as e:
    print(e)
    print('插入失败')
    conn.rollback()    # 回滚事务
finally:
    cur.close()
    conn.close()


'''# 向表中插入多条数据cur.execute()'''
sql = 'insert into t_person (name,age) values (?,?)'
name_list = [('李四', 25), ('小红', 24), ('小李', 12),('张三', 23)]
try:
    # 执行sql语句
    # cur.execute(sql, ('张三', 24))
    cur.executemany(sql,name_list)
    # 提交事务
    conn.commit()
    print('插入成功')
except Exception as e:
    print(e)
    print('插入失败')
    conn.rollback()    # 回滚事务
finally:
    cur.close()
    conn.close()