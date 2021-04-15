#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_cprofile.py
# @Author: Lizi
# @Date  : 2020/11/3

import cProfile
import pstats
from test_pytest import test_function

cProfile.run('test_function.Test_function_demo','test_analyse')

p = pstats.Stats('test_analyse')
p.strip_dirs().sort_stats('line').print_stats()
p.dump_stats('aaa')
p.print_callees()
