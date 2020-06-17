# -*- coding:utf-8 -*-
# @Filename : test39.py 
# @Author : Lizi
# @Time : 2020/2/28 19:01 
# @Software: PyCharm

# 将以数指定的日期打印出来
months=["January","February","March","April","May","June","July","Augest","September","October","November","December"]
endings=["st","nd","rd"] + 17 * ["th"]

year = input("Year: ")
month = input("Month (1-12): ")
day =input("Day (1-31): ")

# 将表示月和日的数减1，得到正确的月份和日期的索引值
# int(month)是将字符型转换成整型
month_name = months[int(month)-1]
ordinal = day + endings[int(day)-1]

print(month + ' ' + ordinal + ' ' + year)