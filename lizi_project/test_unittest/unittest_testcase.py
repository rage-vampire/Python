#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : unittest_test.py
# @Author: Lizi
# @Date  : 2020/11/2

import unittest
import pysnooper
from test_unittest import my_math



class Math_testcase(unittest.TestCase):

    def setUp(self):
        print("-----------------init unit test----------------")

    def tearDown(self):
        print("---------------------done---------------------")

    @pysnooper.snoop(prefix='test_add_init:')
    def test_add_init(self):
        self.assertEqual(first=3, second=my_math.add(1, 2))

    @pysnooper.snoop(prefix='test_add_float:')
    def test_add_float(self):
        self.assertEqual(first=3.789, second=my_math.add(3, 0.789))

    @pysnooper.snoop(prefix='test_add_string:')
    def test_add_string(self):
        self.assertEqual(first="abcdefg", second=my_math.add("ab", "cdefg"))

    # **********************************************************************************************************************
    @pysnooper.snoop()
    def test_sub_int(self):
        self.assertTrue(5 == my_math.sub(105, 100))

    @pysnooper.snoop()
    def test_sub_float(self):
        self.assertNotEqual(first=5.78, second=my_math.sub(10.79, 5.01))  # 这里不等，思考一下为什么呢？

    @pysnooper.snoop()
    def test_sub_float2(self):
        self.assertAlmostEqual(first=5.78, second=my_math.sub(10.79, 5.01), places=2)

# **********************************************************************************************************************
    @pysnooper.snoop()
    def test_multi_number(self):
        self.assertEqual(first=24, second=my_math.multi(3, 8))

    @pysnooper.snoop()
    def test_multi_list(self):
        self.assertListEqual(list1=['th', 'th', 'th', 'th', 'th', 'th'], list2=my_math.multi(6, ['th']))

    @pysnooper.snoop()
    def test_multi_str(self):
        self.assertMultiLineEqual(first="aaaaaaaaaaaaaaaaa", second=my_math.multi(17, "a"))
        self.assertFalse("0123456789" == my_math.multi(8, "0"))
# **********************************************************************************************************************

    @pysnooper.snoop()
    def test_div_int(self):
        self.assertEqual(first=5, second=my_math.div(100, 20))

    @pysnooper.snoop()
    def test_div_float(self):
        self.assertNotEqual(first=0.33333, second=my_math.div(1, 3))

    @pysnooper.snoop()
    def test_div_float2(self):
        self.assertAlmostEqual(first=0.33333, second=my_math.div(1, 3), places=5)

    @pysnooper.snoop()
    def test_div_exception(self):
        with self.assertRaises(Exception):
            my_math.div(1, 0)


if __name__ == "__main__":
    '''verbosity<=0：输出结果中不提示执行成功的用例数；
       verbosity=1：输出结果中仅以.表示执行成功的用例数；
       verbosity>=2：可以输出每个测试用例的执行信息，特别是在大批量时能够清楚的定位出错的测试用例；'''
    unittest.main(verbosity=2)
