#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 斐波那契数列.py
# @Author: Lizi
# @Date  : 2020/12/23

class fibonacci_based_iterator(object):
    """基于迭代器的斐波那契数列"""

    def __init__(self, sequence_count=10):
        self._first = 0
        self._second = 1
        self._sequence_count = sequence_count

        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1
        if self._index == 1:
            return self._first  # 返回数列的第一项
        elif self._index == 2:
            return self._second  # 返回数列的第二项
        elif self._index <= self._sequence_count:
            self._first, self._second = self._second, self._first + self._second  # 这是 Python 的语法糖，把 self._second 赋值给 self._first ，把 self._first+self._second 的和赋值给 self._second
            return self._second  # 返回数列的第 n 项，其中 n >= 3
        else:
            raise StopIteration


def fibonacci_based_generator(sequence_count=10):
    """基于生成器的斐波那契数列"""
    first = 0
    second = 1
    for index in range(0, sequence_count):
        if index == 0:
            yield first
        elif index == 1:
            yield second
        else:
            first, second = second, first + second
            yield second


if __name__ == "__main__":
    fi = fibonacci_based_iterator(sequence_count=20)
    print("基于迭代器的斐波那契数列：")
    for item in fi:
        print(item, end=" ")

    print()

    print("基于生成器的斐波那契数列：")
    fi = fibonacci_based_generator(sequence_count=20)
    for item in fi:
        print(item, end=" ")