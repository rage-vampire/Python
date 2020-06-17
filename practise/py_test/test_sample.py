# -*- coding:utf-8 -*-
# @Filename : test_sample.py 
# @Author : Lizi
# @Time : 2020/4/14 8:58 
# @Software: PyCharm

import pytest

def fun(x):
    return x * x

def test_fun():
    assert (fun(3) == 9)


if __name__ == '__main__':
    pytest.main(['-s', 'test_sample.py'])
