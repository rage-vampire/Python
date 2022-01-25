#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : seek_tell.py
# @Author: Lizi
# @Date  : 2020/10/8

'''seek(offset, whence),offset 表示偏移量，whence表示要从哪个位置开始便宜，0表示从文件开头开始偏移，1表示从当前位置，2表示从文件末尾开始'''
'''tell()返回文件的当前位置'''

with open('test.txt', 'rb') as f:
    print(f.read())
    f.seek(1, 0)
    print(f.tell())
    # print(f.read())
    f.seek(3, 1)
    print(f.tell())
