#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : iter.py
# @Author: Lizi
# @Date  : 2020/12/23


class Interator_counter:
    """声明一个获取迭代次数的类"""

    def __init__(self, max_iter_counter=10):
        self._iter_counter = 0
        self._max_iter_counter = max_iter_counter

    def __next__(self):
        """实现__next__方法，让这个类的对象支持迭代"""
        if self._iter_counter >= self._max_iter_counter:  # 当迭代次数大于等于_max_iter_counter,则抛出StopIteration异常
            raise StopIteration
        else:
            self._iter_counter += 1
            return self._iter_counter

    def __iter__(self):
        return self


if __name__ == '__main__':
    rn = Interator_counter()
    print(next(rn))  # 进行一次迭代，next 函数会调用 iterator_counter 类的 __next__ 方法
    print(next(rn))
    print(next(rn))
    print(next(rn))
    print("enter for loop:")
    for num in rn:
        print(num)
    #
    # print(next(rn))