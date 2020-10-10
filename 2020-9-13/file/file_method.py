#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : file_method.py
# @Author: Lizi
# @Date  : 2020/10/8

import sys
text = sys.stdin.read()
words = text.split()
wordcount = len(words)
print(wordcount)