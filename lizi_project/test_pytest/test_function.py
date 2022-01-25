#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_function.py
# @Author: Lizi
# @Date  : 2020/11/2

import pytest
import function_demo

class Test_function_demo:
    def setup(self):
        print("---------------------开始测试--------------------\n")

    def teardown(self):
        print('----------------------done----------------------\n')

    # @pytest.mark.slow
    def test_add_int(self):
        assert (function_demo.add(2, 3) == 5)

    # @pytest.mark.faster
    def test_add_float(self):
        assert (function_demo.add(3, 0.789) == 3.789)

    def test_add_string(self):
        assert (function_demo.add('aa', 'bb') == 'aabb')

    def test_sub_int(self):
        assert (function_demo.sub(10, 7) == 3)

    @pytest.mark.xfail
    def test_sub_float(self):
        assert (function_demo.sub(10.79, 5.01) != 5.78)



if __name__ == '__main__':
    pytest.main(['-s', 'test_function.py', '--html=report/report.html'])