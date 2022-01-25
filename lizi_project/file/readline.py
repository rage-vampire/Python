#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : readline.py
# @Author: Lizi
# @Date  : 2020/10/8


# with open('test.txt', 'r+') as f:
#     for i in range(3):
#         print(i, f.readline())
#         # print(i, f.readlines())


def read():
    '''每次一个字符'''
    with open('somefile.txt') as f:
        while True:
            char = f.read(1)
            if not char:
                break
            print(char)

#
def readline():
    '''每次一行'''
    with open('somefile.txt') as f:
        while True:
            char = f.readline()
            if not char:
                break
            print(char, end='')
#
with open('somefile.txt') as f:
    for line in f:
        print(line,end='')


# if __name__ == '__main__':
#     readline()
    # read()