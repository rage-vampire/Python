#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : cal.py
# @Author: Lizi
# @Date  : 2020/10/10
import calendar

yy = int(input("please enter year:"))
mm = int(input("please enter month:"))

print(calendar.month(yy, mm))