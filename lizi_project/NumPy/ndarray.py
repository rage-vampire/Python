# -*- coding: utf-8 -*-
# @Date : 2022/1/19 15:12
# @File : ndarray.py
# @Author : Lizi

import numpy as np

'''
创建一个ndarray：调用NumPy中的array函数
    numpy.array(object, dtype = None, copy = True, order = None, subok = False, ndmin = 0)
    object：数组或嵌套的数列
    dtype：数组元素的数据类型
    copy：对象是否需要复制
    order：创建数组的样式，C为行方向、F为列方向、A为任意方向（默认）
    subok：默认返回一个与基类类型一致的数组
    ndmin：指定生成数组的最小维度
    
'''

nd_1 = np.array([1,2,3])
nd_2 = np.array([[1,2,3],[4,5,6]])

print('一维数组:',nd_1)
print('二维数组:\n',nd_2)