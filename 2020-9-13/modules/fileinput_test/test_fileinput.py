#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_fileinput.py
# @Author: Lizi
# @Date  : 2020/9/23

import fileinput
'''fileinput_test.input (files=None, inplace=False, backup='', bufsize=0, mode='r', openhook=None)
file:文件的路径列表，默认是stdin方式，多文件['1.txt','2.txt',...]
inplace:是否将标准输出的结果写回文件，默认不取代
backup：备份文件的扩展名，如果备份文件存在，则覆盖
bufsize：缓冲区大小，默认为0
mode：读写模式，默认为只读
'''
# 打印指定文件的所有行，且将原文件备份,并将原文件中的字符a替换成perl
for lines in fileinput.input('fileinput_test',inplace=True, backup='.bak'):
    print(lines.rstrip().replace('a','perl'))
    # print(fileinput_test.filename())


'''给文件添加行号'''
for lines in fileinput.input(['fileinput_test','aa'], inplace=1):
    line = lines.rstrip()
    num = fileinput.filelineno()   # filelineno()处理完一个文件后，将重置编号，处理下个文件时从1开始编号
    # num = fileinput_test.lineno()       # ineno()处理完一个文件后，不会重置编号，处理下个文件时将从上个文件的最后一行的行号继续编号
    print('{:<} # {}'.format(line,num))