#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_sys.py
# @Author: Lizi
# @Date  : 2020/9/22

import pprint
import sys

print(sys.argv)
'''sys.argv命令行参数，返回一个命令行参数列表，sys.argv[0]表示脚本名称'''
for i in range(len(sys.argv)):
    print("argv{}:type is {},value is: {}".format(i, type(sys.argv[i]), sys.argv[i]))

'''sys.path一个列表，包含要在其中查找模块的目录名称。sys.path[0] 表示当前脚本所在目录'''
pprint.pprint(sys.path)

'''sys.modules返回一个已加载模块的字典，将模块名映射到加载的模块'''
pprint.pprint(sys.modules)

'''sys.exc_info() 获取正在处理的异常的相关信息.返回值为一个包含异常类、异常实例和异常回溯信息的元组'''

s = 'hjkf'
try:
    int(s)
except ValueError:
    # raise
    e = sys.exc_info()
    print(e)
    print(type(e))

