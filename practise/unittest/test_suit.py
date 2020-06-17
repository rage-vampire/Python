# -*- coding:utf-8 -*-
# @Filename : test_suit.py 
# @Author : Lizi
# @Time : 2020/4/10 19:21 
# @Software: PyCharm

import unittest
from unit_test import ProductTestCase

if __name__ == '__main__':
    suite = unittest.TestSuite()
    tests = [ProductTestCase('test_int'),ProductTestCase("test_float")]
    suite.addTests(tests)
    with open("test.txt",'a') as f:
        runner = unittest.TextTestRunner(stream=f,verbosity=2)
        runner.run(suite)