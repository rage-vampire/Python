#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : operator.py
# @Author: Lizi
# @Date  : 2020/9/8
a = 10
b = 20

def operator():
    if (a and b):
        print('1--a 和 b都为True')
    else:
        print('1--a 和 b有一个不为true')
    if (a or b):
        print("2--a 和 b都为true，或有一个为true")
    else:
        print('2--a 和 b都不为true')


if __name__ == '__main__':
    operator()