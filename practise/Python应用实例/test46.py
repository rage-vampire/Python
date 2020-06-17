# -*- coding:utf-8 -*-
# @Filename : test46.py 
# @Author : Lizi
# @Time : 2020/3/26 14:35 
# @Software: PyCharm

import pprint
# import sys
import fileinput
import os
import random
import time


def time():
    date1 = (2016,1,1,0,0,0,-1,-1,-1)
    time1 = time.mktime(date1)
    date2 = (2017,1,1,0,0,0,-1,-1,-1)
    time2 = time.mktime(date1)
    print(time1)
    random_time = random.uniform(time1,time2)
    print(time.asctime(time.localtime(random_time)))


def side():
    sum = 0
    num = int(input("有几个骰子："))
    sides = int(input("每个骰子多少面："))
    for i in range(num):
        sum += random.randrange(sides) + 1
    print(sum)


def kk():
    # deck = []
    values = list(range(1,11)) + 'Jack Queen King'.split()
    print(values)

    result=[]
    suits = "diamonds clubs hearts spades".split()

    for v1 in values:
        for v2 in suits:
            result.append('{} of {}'.format(v1,v2))

    #deck = ["{} of {}".format(v,s) for v in values for s in suits]
    #random.shuffle(deck)
    #pprint.pprint(deck)
    pprint.pprint(result)


if __name__ == "__main__":
    kk()