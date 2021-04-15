#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test__suite.py
# @Author: Lizi
# @Date  : 2020/11/2


import unittest
from unittest_testcase import Math_testcase as testcase
from BeautifulReport import BeautifulReport
# from .unittest_testcase import Math_testcase as testcase

if __name__ == '__main__':
    suite = unittest.TestSuite()
    # tests = [testcase('setUp'), testcase('tearDown'), testcase('test_add_init'),testcase('test_sub_int'),
    #          testcase('test_sub_float'),testcase('test_sub_float2'), testcase('test_multi_list'),
    #          testcase('test_multi_str'), testcase('test_div_int'),testcase('test_div_float'),
    #          testcase('test_div_float2'),testcase('test_div_exception')]
    tests = unittest.TestLoader().loadTestsFromTestCase(testCaseClass='testcase')
    suite.addTests(tests)
    with open('test_report', 'w') as file:
        runner = unittest.TextTestRunner(stream=file, descriptions=True, verbosity=2)
        runner.run(suite)

