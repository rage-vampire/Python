#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : run_nian.py
# @Author: Lizi
# @Date  : 2020/9/8

'''判断用户输入的年份是否为闰年'''
def nian(year):
    if year % 400 == 0:
        print("{0}是世纪润年！".format(year))
    elif year % 4 == 0:
        print("{0}是普通润年!".format(year))
    else:
        print('{0}不是闰年！'.format(year))

if __name__ == '__main__':
    year = int(input("请输入年份："))
    nian(year)