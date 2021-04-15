#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 杨辉三角.py
# @Author: Lizi
# @Date  : 2020/12/23


class pascal_triangle_based_iterator(object):
    """基于迭代器的杨辉三角"""

    def __init__(self, level_count=10):
        self._level_count = level_count
        self._sequence = [1]
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1
        if self._index == 1:
            return self._sequence
        elif self._index <= self._level_count:
            current_sequence = [1]
            left_num = 1
            for item in self._sequence[1:]:
                current_sequence.append(left_num+item)
                left_num = item
            current_sequence.append(1)
            self._sequence = current_sequence
            return self._sequence
        else:
            raise StopIteration


if __name__ == "__main__":
    pascaler = pascal_triangle_based_iterator(level_count=10)
    print("基于迭代器的杨辉三角：")
    for item in pascaler:
        print(" ", f"{item}".center(40, " "))

