#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : ddt_demo.py
# @Author: Lizi
# @Date  : 2020/12/1

import ddt
from ddt import ddt, data, unpack, file_data
import unittest
from selenium import webdriver


# @ddt()
# class TestCase(unittest.TestCase):
#     # test_data = 'yanglili'
#
#     test_data = ('admin', 'yanglii')
#
#     # 通过*号进行解包，每一个值都是一条测试用例
#     @data(*test_data)
#     def test_01(self, username):
#         print(username)


# @ddt()
# class TestCase(unittest.TestCase):
#     # test_data = 'yanglili'
#
#     # 通过*号进行解包，每一个元祖都是一条测试用例
#     test_data = [('admin', 123456), ('yanglili', 8888)]
#
#     @data(*test_data)
#     # @unpack
#     def test_01(self, username):
#         print(username)
#         print('测试用例1')


# @ddt()
# class TestCase(unittest.TestCase):
#     # test_data = 'yanglili'
#
#     # test_data = [('admin', 123456), ('yanglili', 8888)]
#     test_data = [['admin', 123456], ['yanglili', 8888]]
#
#     # 通过*号进行解包，每一个元祖/列表都是一条测试用例
#     @data(*test_data)
#     @unpack  # 使用unpack对元祖或者列表进行解包
#     def test_01(self, username, pwd):
#         print(username, pwd)
#         print('测试用例1')


# @ddt()
# class TestCase(unittest.TestCase):
#     # test_data = 'yanglili'
#
#     # 通过*号进行解包，每一个元祖都是一条测试用例
#     @data(*[('admin', 123456), ('yanglili', 8888)])
#     @unpack  # 使用unpack对元祖或者列表进行解包
#     def test_01(self, username, pwd):
#         print(username, pwd)
#         print('测试用例1')

"""
    使用yaml文件，数据驱动
"""
# @ddt()
# class TestCase(unittest.TestCase):
#     # test_data = 'yanglili'
#
#     @file_data('./test.yaml')
#     def test_01(self, **test_data):
#         print(test_data)

driver = webdriver.Chrome()
driver.get('http://www.baidu.com')


# if __name__ == '__main__':
#     unittest.main()
