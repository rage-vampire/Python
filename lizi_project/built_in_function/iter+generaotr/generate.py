#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : generate_02.py
# @Author: Lizi
# @Date  : 2020/12/23


def generate_even(number_count: int = 5):
    """返回偶数序列的生成器"""
    num = 0
    for index in range(0, number_count):
        print("yield...{0}".format(num))
        yield num  # yield 与 return 不同，yield 的执行流程是先暂停当前函数的执行，然后返回 num 的值给调用函数，调用函数执行完成后再返回到本函数的 yield 处继续执行
        num += 2
        print("yield")


if __name__ == "__main__":
    for num in generate_even():  # 生成 5 个偶数
        print("num的值为:{}".format(num))


