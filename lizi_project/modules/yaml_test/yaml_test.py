#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : yaml_test.py
# @Author: Lizi
# @Date  : 2020/11/11

import yaml

list_test = [1, 2, 3, 4, True, 'lizi', '杨丽丽']

with open('demo.yaml', 'w') as f:
    yaml.dump_all(list_test, f, allow_unicode='utf-8')
