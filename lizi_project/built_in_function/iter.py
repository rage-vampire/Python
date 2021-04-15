#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : iter.py
# @Author: Lizi
# @Date  : 2020/12/17

import sys

list1 = (12, 4, 6, 7, 10)
it = iter(list1)

while True:
    try:
        print(next(it))
    except StopIteration:
        sys.exit()