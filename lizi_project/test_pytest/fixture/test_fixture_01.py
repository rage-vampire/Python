#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_fixture_01.py
# @Author: Lizi
# @Date  : 2021/4/19

import pytest


class Fruit:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        self.name = other.name


@pytest.fixture
def my_fruit(self):
    """定义了一个fixture，返回了一个Fruit对象，名字为Apple"""
    return Fruit('Apple')


# fixture调用fixture
@pytest.fixture
def fruit_basket(my_fruit):
    """定义了另一个fixture，同样声明了一个Fruit对象，名字为Banner
    然后在这个fixture中传入了上一个fixture：my_fruit
    最终将结果返回到一个列表中"""
    return [Fruit('Banner'), my_fruit]


# 测试函数声明传参请求fixture
def test_my_fruit_in_basket(my_fruit, fruit_basket):
    """这是一个测试函数，可以使用多个fixture"""
    assert my_fruit in fruit_basket


if __name__ == '__main__':
    pytest.main()