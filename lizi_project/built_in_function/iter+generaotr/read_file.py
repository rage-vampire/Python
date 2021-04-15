#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : read_file.py
# @Author: Lizi
# @Date  : 2020/12/23
import sys


def process_txt_file(file_name:str):

    """
    1、把这个文本文件的所有行的首尾空格全部删除；
    2、并在每行前面增加行号，即：第一行的行号为1，第二行的行号为2；
    3、处理完成后，交给你的其他同事继续进行处理。
    """
    with open(file_name, 'r', encoding='utf-8') as file:
        line_num = 1
        for line in file:
            new_line = line.strip()
            new_line = f'{line_num} {line}'
            yield new_line
            line_num += 1


if __name__ == '__main__':
    file_name = sys.argv[0]
    # print(file_name)
    for line in process_txt_file(file_name):
        print(line, end=' ')