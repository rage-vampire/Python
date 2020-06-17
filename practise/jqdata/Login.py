# -*- coding:utf-8 -*-
# @Filename : Login.py 
# @Author : Lizi
# @Time : 2020/4/2 15:00 
# @Software: PyCharm
from datetime import date

from jqdatasdk import *
auth('18938896626','896626')
print(get_query_count())

df = finance.run_query(query(finance.FUT_GLOBAL_DAILY).filter(finance.FUT_GLOBAL_DAILY.day =='2020-04-02').limit(10))
print(df)
path = r"D:\Py_file\jqdata\test.csv"
df.to_csv(path,sep=',',index=True,header=True,encoding="utf_8_sig")