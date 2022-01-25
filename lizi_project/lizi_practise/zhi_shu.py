#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : zhi_shu.py
# @Author: Lizi
# @Date  : 2020/9/8


num = int(input("请输入一个数："))

if num>=1:
    for i in range(2,num):    # 查看因子项
        if num % i == 0:      # 遍历除所有的因子，如果余数为0，则不是质数
            print('{}不是质数！'.format(num))
            print(i,'乘以',num//i,'等于',num)
            break             # 不是质数到此结束，不再执行后面的代码
    else:
        print('{}是质数！'.format(num))
else:
    print('{}不是质数！'.format(num))