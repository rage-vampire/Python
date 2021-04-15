#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_random.py
# @Author: Lizi
# @Date  : 2020/9/24

import random


'''生成0-1（含）的随机实数'''
print(random.random())

'''random_test.uniform(a, b)生成a-b（含）的随机实数'''
print(random.uniform(1, 8.9))


'''random_test.randrange()随机选择一个数'''
print(random.randrange(2,10,2))

random.choice()
random.sample()
random.shuffle()