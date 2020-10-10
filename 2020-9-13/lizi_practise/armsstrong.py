#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : armsstrong.py
# @Author: Lizi
# @Date  : 2020/10/10

num = int(input('please enter num : '))
n = len(str(num))

sum = 0
temp = num
while temp > 0:
    digit = temp % 10
    sum += digit ** n
    temp = temp // 10

if num == sum:
    print(num,'是阿姆斯特朗数')
else:
    print(num,'不是阿姆斯特朗数')