#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : input_output.py
# @Author: Lizi
# @Date  : 2020/10/10

'''repr()： 产生一个解释器易读的表达形式。'''

s = 'hello world'
x = 10 * 3.5
y = 20 * 7
print(repr(s))
print(repr(x), repr(y))

'''repr()函数可以转义字符串中的特殊字符串'''
i = 'hello python\n'
print(repr(i))

'''repe()参数可以是Python的任意对象'''
print(repr((x, y, ('aa', 'bb', 124))))

'''实例1：输出一个平方和一个立方的表'''
for i in range(1,11):
    print('{0:>2d},{1:>3d},{2:>4d}'.format(i, i*i, i*i*i))


'''实例2：字典的格式化'''
table = {'Google': 1, 'Runoob': 2, 'Taobao': 3}
print('Google:{Google}, Runoob:{Runoob}, Taobao:{Taobao}'.format_map(table))
print('Google:{Google}, Runoob:{Runoob}, Taobao:{Taobao}'.format(**table))