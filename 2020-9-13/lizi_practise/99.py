#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 99.py
# @Author: Lizi
# @Date  : 2020/9/7

def multi99():
    for i in range(1, 10):
        for j in range(1, i+1):
            print('{}*{}={}'.format(j, i, i*j),end=' ')
        print('')

def multi():
    for i in range(1, 10):
        for j in range(i,10):
            print('{}*{}={}'.format(i, j, i*j),end=' ')
        print('')


if __name__ == '__main__':
    multi99()
    print('-------------------------------------------------------------')
    multi()

