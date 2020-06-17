# -*- coding: utf-8 -*-
# @file   : test35.py
# @author : lizi
# @date   : 2019/11/20
# @version: 1.0
# @desc   :

'斐波那契数数列：每个数都是前两个数的和'
def fibs(num):
    '创建result列表'
    result = [0,1]
    for i in range (num):
        result.append(result[-2] + result[-1])
    print(result)
fibs(20)
print(fibs.__doc__)   #__doc__是函数的一个属性，用来访问函数内的字符串