#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : generate_02.py
# @Author: Lizi
# @Date  : 2020/12/23

def generate_even(number_counter: int = 5):
    num = 0
    for index in range(0, number_counter):
        # print("yield......{}".format(num))
        yield num
        num += 2


def generate_odd(number_counter: int = 5):
    num = 1
    for index in range(0, number_counter):
        # print("yield......{}".format(num))
        yield num
        num += 2


if __name__ == "__main__":
    names = ["Tom", "Tim", "Jim", "Ada"]
    generates = [generate_even(5), generate_odd(5), names, "done.", 1234]  # 构造一个列表
    # print(generates)

    def travel_generate():
        """
            yield from:只能用于可迭代对象（如：生成器、列表、字符串、元祖、字典、集合等）
        """
        for ele in generates:
            if hasattr(ele, "__iter__"):
                # print(f'__iter__属性值：{ele.__iter__()}')
                yield from ele
            else:
                yield ele

    for item in travel_generate():
        print(item)
