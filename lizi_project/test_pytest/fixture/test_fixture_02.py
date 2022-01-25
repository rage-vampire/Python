#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_fixture_02.py
# @Author: Lizi
# @Date  : 2021/4/19

import pytest


# Arrange
@pytest.fixture
def fruit_bowl():
    return ["苹果", "香蕉"]


# fixture中的返回值传递给测试函数（测试用例）
def test_fruit_salad(fruit_bowl):
    # Act
    fruit_salad = fruit_bowl[0] + fruit_bowl[1]

    # Assert
    assert fruit_salad == "苹果香蕉"


if __name__ == '__main__':
    pytest.main(['-s'])