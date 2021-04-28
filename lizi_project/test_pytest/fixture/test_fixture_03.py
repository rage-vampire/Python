#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_fixture_03.py
# @Author: Lizi
# @Date  : 2021/4/21


import pytest

"""Fixture的复用性"""
"""test_stringhe test_int函数都调用了fixture函数order，但是并不影响各自的值"""


@pytest.fixture()
def first_entry():
    return 'a'


@pytest.fixture()
def order(first_entry):
    return [first_entry]


def test_string(order):
    order.append('b')
    assert order == ['a', 'b']


def test_int(order):
    order.append(2)
    assert order == ['a', 2]


if __name__ == '__main__':
    pytest.main(['test_fixture_03.py'])