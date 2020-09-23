#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_os.py
# @Author: Lizi
# @Date  : 2020/9/22

import os
import sys
import pprint



'''os.environ返回一个字典，包含系统的环境变量'''
# pprint.pprint(os.environ.values())
# for item in os.environ.items():
#     print(item)


''' os.sep用于路径名中的分割符号，在Windows中表示为\，在Unix中表示为/'''
# data_dir = os.sep.join(['hello', 'world'])   # 用\连接两个字符
# environ_dir = os.environ['PATH'].split(os.sep)  # 按\拆分字符
#
# print(data_dir)
# print(environ_dir)
#
# '''os.pathsep'''
# data_dir1 = os.pathsep.join(['hello', 'world'])    # 用;连接两个字符
# environ_dir1 = os.environ['PATH'].split(os.pathsep)      # 按;拆分两个字符
# print(data_dir1)
# print(environ_dir1)

'''os.startfile实现双击运行程序'''
# os.startfile(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')

# print(os.name)
# print(os.getcwd())       # 获取当前工作的目录
# print(os.path.abspath('./'))    # 获取文件或文件夹的绝对路径
# print(os.listdir('./'))  # 返回一个包含当前目录下所有的文件和目录的列表。"./"表示当前目录，“../”表示上级目录，也可接具体的绝对路径
# os.path.isfile('path')    # 判断指定对象是否为文件，是返回true，否则放回false
# os.path.isdir('path')     # 判断指定对象是否为目录，是返回true，否则放回false
# os.remove('path')    # 删除path路径下指定的文件
# os.rmdir('path')    # 删除path路径下指定的目录
# os.mkdir('path')    # 创建path路径下指定的目录，只能建立一层。os.makedirs()可递归创建
# os.path.exists('path')   # 判断文件是否存在，存在返回true，否则返回false
# print(os.path.getsize('test_sys.py'))    # 获得文件的大小，如果为目录，返回0

print(os.path.split(r'E:\Python\2020-9-13\lizi_practise'))    # os.path.split()返回路径的目录和文件（夹）名，将目录和文件（夹）名分开，即找到最后一个\，将整个路径拆分
print(os.path.join('path', 'name'))     # 连接目录和文件名

print(os.path.basename(r'E:\Python\2020-9-13\modules\test_os.py'))   # 返回文件名
print(os.path.dirname(r'E:\Python\2020-9-13\modules\test_os.py'))   # 返回目录



# path = os.listdir('../')
# print(path)
# for files in path:
#     if os.path.isfile(files):
#         print('这是文件：', files)
#     if os.path.isdir(files):
#         print('这是目录：', files)