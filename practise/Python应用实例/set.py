# -*- coding:utf-8 -*-
# @Filename : set.py 
# @Author : Lizi
# @Time : 2020/6/9 14:57 
# @Software: PyCharm

import sys


# 迭代器，斐波那契数
# class Fibs():
#     def __init__(self):
#         self.a = 0
#         self.b = 1
#
#     def __next__(self):
#         self.a, self.b = self.b, self.a+self.b
#         return self.a
#
#     def __iter__(self):
#         return self
#
# if __name__ == '__main__':
#     fib = Fibs()
#     for i in fib:
#         if i > 1000:
#             print(i)
#             break


# 2、生成器

def flatten(nested):
    try:
        for sublist in nested:
            for element in sublist:
                yield element
    except TypeError:
        yield nested



nested = [0, 9, [1, 2], [3, 4]]

# nested = [1, 2, 3, 4, 5,[7, 8]]
for num in flatten(nested):
    print(num)

# print(list(flatten(nested)))
