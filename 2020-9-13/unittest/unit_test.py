# -*- coding:utf-8 -*-
# @Filename : unit_test.py
# @Author : Lizi
# @Time : 2020/4/10 17:17 
# @Software: PyCharm


import unittest, my_math
import pysnooper
from BeautifulReport import BeautifulReport


class test_funcation_demo(unittest.TestCase):
    def setUp(self):
        print("___________________init unit test_________________")

    def tearDown(self):
        print("___________________done___________________________")


class ProductTestCase(unittest.TestCase):
    # @pysnooper.snoop(prefix='test_int: ')
    def test_int(self):
        for x in range(-10, 10):
            for y in range(-10, 10):
                p = my_math.product(x, y)
                self.assertEqual(p, x * y, 'Int failed')

    # @pysnooper.snoop(prefix="test_float:")
    def test_float(self):
        for x in range(-10, 10):
            for y in range(-10, 10):
                x = x / 10
                y = y / 10
                p = my_math.product(x, y)
                self.assertEqual(p, x * y, 'float,faild')



if __name__ == '__main__':
    unittest.main(verbosity=2)
