#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 等差数列.py
# @Author: Lizi
# @Date  : 2020/12/23

class Arithemtic_sequence_based_iterator:
    def __init__(self, first=0, step=1, sequence_count=10):
        self._first = first
        self._step = step
        self._sequence_counter = sequence_count
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < self._sequence_counter:
            res = self._first + self._index * self._step
            self._index += 1
            return res
        else:
            raise StopIteration


def arithemtic_sequence_based_generator(first=0, step=1, sequence_count=10):
    """基生生成器函数的等差数列，与上面的代码功能完全相同"""
    for index in range(0, sequence_count):
        yield first + index * step
        index += 1


if __name__ == '__main__':
    interator = Arithemtic_sequence_based_iterator(first=0, step=5, sequence_count=10)
    print("基于迭代器的等差数列的结果：")
    for num in interator:
        print(num, end=' ')

    print(' ')

    generator = arithemtic_sequence_based_generator(first=0, step=5, sequence_count=10)
    print("基于生成器的等差数列的结果：")
    for num in generator:
        print(num, end=' ')
