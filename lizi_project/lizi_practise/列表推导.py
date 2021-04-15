#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 列表推导.py
# @Author: Lizi
# @Date  : 2020/12/8

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# aa = [[matrix[row][col] for row in range(0, len(matrix))] for col in range(0, len(matrix))]
# print(aa)
#
#
#
# all_list = []
# for row in range(0, len(matrix)):
#     new_list = []
#     for col in range(0, len(matrix)):
#         new_list.append(matrix[col][row])
#     all_list.append(new_list)
# print(all_list)


data = [[7, 2], [3], [0], [8], [1], [4]]


# data = (1, 2, 6, 4, 7, 3, 9)
def min_val(data):
    return max(data, key=lambda x: len(x))


aa = min_val(data)
print(aa)
