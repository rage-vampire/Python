# -*- coding:utf-8 -*-
# @Filename : jie_cheng.py 
# @Author : Lizi
# @Time : 2020/6/22 14:43 
# @Software: PyCharm


def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)

