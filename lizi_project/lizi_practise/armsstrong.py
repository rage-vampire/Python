#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : armsstrong.py
# @Author: Lizi
# @Date  : 2020/10/10

'''实例1：判断用户输入的是否是阿姆斯特朗数'''
# num = int(input('please enter num : '))
# n = len(str(num))
#
# sum = 0
# temp = num
# while temp > 0:
#     digit = temp % 10
#     sum += digit ** n
#     temp = temp // 10
#
# if num == sum:
#     print(num,'是阿姆斯特朗数')
# else:
#     print(num,'不是阿姆斯特朗数')

'''实例2，筛选出指定区间的阿姆斯特朗数'''
for num in range(1, 1000):
    n = len(str(num))
    sum = 0
    temp = num
    while temp > 0:
        digit = temp % 10
        sum += digit ** n
        temp = temp // 10

    if num == sum:
        print(num, '是阿姆斯特朗数')
    # else:
    #     print(num, '不是阿姆斯特朗数')
