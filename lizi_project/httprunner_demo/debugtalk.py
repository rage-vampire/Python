import time


"""
基于约定大于配置的原则，每个项目有且只有一个debugtalk.py，该文件拥有多种功能。

作为项目根路径的锚，测试用例中的相对路径（例如引用测试用例或CSV文件）都基于此根路径。
存储自定义的python函数，在测试用例中调用的函数均在此文件中定义
"""
from httprunner import __version__


def get_httprunner_version():
    return __version__


def sum_two(m, n):
    return m + n


def sleep(n_secs):
    time.sleep(n_secs)
