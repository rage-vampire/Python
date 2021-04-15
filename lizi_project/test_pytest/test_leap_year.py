# -*- coding:utf-8 -*-
# @Filename : test_leap_year.py
# @Author : Lizi
# @Time : 2020/4/20 9:30 
# @Software: PyCharm

import os
import pytest
import allure


def is_leap_year(year):
    if isinstance(year, int) is not True:
        raise TypeError("传入的参数不是整数")
    elif year == 0:
        raise ValueError("公元元年是从公元一年开始的")
    elif abs(year) != year:
        raise TypeError("传入的参数不是正整数！")
    elif year % 4 == 0 and year % 100 == 0:
        print("{}是闰年".format(year))
        return True
    else:
        print("{}不是闰年".format(year))
        return False


class TestAssert:
    @pytest.mark.run(order=2)  # 指定执行顺序
    @pytest.mark.flaky(reruns=6, reruns_delay=2) # 指定重跑的次数，和延时时间
    def test_exception_value01(self):
        with pytest.raises(TypeError):
            is_leap_year('ss')

    @pytest.mark.run(order=3)
    def test_true(self):
        assert is_leap_year(2017) == True

    # 将异常信息存储到变量中，变量的类型就是异常类，包含异常的type，value和traceback
    def test_exception_value02(self):
        with pytest.raises(ValueError) as excinfo:
            is_leap_year(0)
            assert excinfo.type == ValueError
            assert "从公元一年开始" in str(excinfo.value)

    # """定义用例中抛出的异常信息是否与预期的异常信息匹配，若不匹配则用例执行失败，match关键词参数传递给上下文管理器，
    # 以测试正则表达式与异常的字符串表示形式是否匹配，这种方法只能断言value，不能断言type"""
    def test_exception_match(self):
        with pytest.raises(ValueError, match='公元33元年是从公元一年开始') as excinfo:
            is_leap_year('y')
            pytest.assume
            assert excinfo.type == TypeError
            assert excinfo.type == ValueError

    # 使用标记函数检查异常,当抛出的异常与raises的异常相同时，则执行通过，否则执行失败
    @pytest.mark.run(order=1)
    @pytest.mark.xfail(raises=TypeError)
    def test_typeError(self):
        is_leap_year('ss')


if __name__ == '__main__':
    pytest.main(['-s', 'test_leap_year.py'])
