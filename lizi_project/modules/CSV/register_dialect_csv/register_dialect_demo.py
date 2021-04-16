#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : register_dialect_demo.py
# @Author: Lizi
# @Date  : 2021/4/16

import csv

"""
自定义dialect的值
delimiter="|":以|为分割符
quoting=csv.QUOTE_ALL：
"""
csv.register_dialect('mydialect', delimiter="|", quoting=csv.QUOTE_MINIMAL)

with open('./demo_1.csv', 'r') as csvfile:
    reader_file = csv.reader(csvfile, dialect='mydialect')
    for row in reader_file:
        print(row)

print(csv.list_dialects())
print(csv.get_dialect('mydialect'))