#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_function.py
# @Author: Lizi
# @Date  : 2020/11/2

import pytest
import function_demo

class Test_function_demo:
    def setup(self):
        print("---------------------开始测试--------------------")

    def teardown(self):
        print('----------------------done----------------------')

    # @pytest.mark.slow
    def test_add_int(self):
        assert (function_demo.add(2, 3) == 5)

    # @pytest.mark.faster
    def test_add_float(self):
        assert (function_demo.add(3, 0.789) == 3.789)

    def test_add_string(self):
        assert (function_demo.add('aa', 'bb') == 'aabb')


if __name__ == '__main__':
    pytest.main(['-s', 'test_function.py', '--html=report/report.html'])