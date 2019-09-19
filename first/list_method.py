# -*- coding: utf-8 -*-
# @file   : list_method.py
# @author : lizi
# @date   : 2019/9/18
# @version: 1.0
# @desc   :

names = ['yang','lili','qingqing','yanyan','yiyi']
num = [1,2,0,4,8,5,4,9,66,55]
#反向排序
num.reverse()
print("reverse后的值:",num)
#默认升序排序)
num.sort()
print("sort后的值:",num)
#a按长度降序排序
names.sort(key=len,reverse=True)
print(names)