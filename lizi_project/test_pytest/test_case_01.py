# -*- coding:utf-8 -*-
# @Filename : test_case_01.py 
# @Author : Lizi
# @Time : 2020/4/17 8:47 
# @Software: PyCharm

import pytest


def test_case01():
    print('执行用例01......')
    assert 1  # 断言成功


def test_case02():
    print("执行用例02........")
    assert 1  # 断言成功


class TestCaseClass:
    def test_case03(self):
        print('执行用例03......')
        assert 0  # 断言失败
