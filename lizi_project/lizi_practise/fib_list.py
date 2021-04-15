#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : fib_list.py
# @Author: Lizi
# @Date  : 2020/9/7

'''斐波那契数列'''


def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n - 2) + fib(n - 1)


if __name__ == '__main__':
    for n in range(10):
        print(fib(n),end=' ')
