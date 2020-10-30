# -*- coding:utf-8 -*-
# @Filename : test_function_demo.py
# @Author : Lizi
# @Time : 2020/3/9 10:54 
# @Software: PyCharm
import os
import traceback
from datetime import time
from random import random

from BeautifulReport import BeautifulReport
import function_demo
import unittest
import pysnooper


class Test_function_demo(unittest.TestCase):

    def setUp(self):
        print("___________________init unit test_________________")

    def tearDown(self):
        print("___________________done___________________________")

    # **************************************************************************************************
    # @unittest.expectedFailure
    @pysnooper.snoop(prefix='_add_int ')
    def test_add_int(self):
        try:
            self.assertNotEqual(first=3, second=function_demo.add(1, 2), msg='first等于second')
        except AssertionError as e:
            raise e
            print(e)

    # **************************************************************************************************
    @pysnooper.snoop(prefix='_sub_int ')
    def test_sub_int(self):
        self.assertTrue(5 == function_demo.sub(105, 100))

    # **************************************************************************************************
    @pysnooper.snoop(prefix='_sub_float ')
    def test_sub_float(self):
        self.assertNotEqual(first=5.78, second=function_demo.sub(10.79, 5.01))

    # **************************************************************************************************
    # @unittest.skip("test_sub_float2：用例不需要测试")  # 跳过测试
    @pysnooper.snoop(prefix='_sub_float2 ')
    def test_sub_float2(self):
        self.assertAlmostEqual(first=5.78, second=function_demo.sub(10.79, 5.01), places=2)

    # **************************************************************************************************
    @pysnooper.snoop(prefix='_multi_list ')
    def test_multi_list(self):
        self.assertListEqual(list1=['th', 'th', 'th', 'th', 'th', 'th'], list2=function_demo.multi(6, ['th']))

    # **************************************************************************************************
    @pysnooper.snoop(prefix='_multi_str ')
    def test_multi_str(self):
        self.assertMultiLineEqual(first="aaaaa", second=function_demo.multi(5, "a"))
        self.assertFalse("0123456789" == function_demo.multi(8, "0"))

    # **************************************************************************************************
    @pysnooper.snoop(prefix='_div_int ')
    def test_div_int(self):
        self.assertEqual(first=5, second=function_demo.div(100, 20))
        self.assertTrue(5 == function_demo.div(100, 20))

    # **************************************************************************************************
    @pysnooper.snoop(prefix='_div_float ')
    def test_div_float(self):
        self.assertNotEqual(first=0.3333, second=function_demo.div(1, 3))

    # **************************************************************************************************
    # @unittest.expectedFailure         # 预期失败，若实际结果为失败，则表示测试通过；若实际结果为通过，则表示测试不通过
    @pysnooper.snoop(prefix='_div_float2 ')
    def test_div_float2(self):
        self.assertAlmostEqual(first=0.3333, second=function_demo.div(1, 3), places=4)

    # **************************************************************************************************
    @pysnooper.snoop(prefix='_div_exception ')
    def test_div_exception(self):
        with self.assertRaises(Exception):
            function_demo.div(1, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
