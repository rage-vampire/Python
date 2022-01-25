# -*- coding: utf-8 -*-
# @Date : 2022/1/19 15:34
# @File : NumPy_attribute.py
# @Author : Lizi
import numpy as np

"""
数组的属性：
    1、ndarray.ndim：秩，即轴的数量或维度的数量（类似于三位空间中的X、Y、Z轴）
     一维数组的秩为1、二维数组的秩为2，以此类推
    2、ndarray.shape：数组的维度，对于矩阵，n行m列
    3、ndarray.size：数组元素的总个数，相当于 .shape 中 n*m 的值
    4、ndarray.dtype：ndarray 对象的元素类型
    5、ndarray.itemsize：ndarray 对象中每个元素的大小，以字节为单位
    6、ndarray.flags：ndarray 对象的内存信息
    7、ndarray.real：ndarray元素的实部
    8、ndarray.imag;ndarray元素的虚部
    9、ndarray.data：包含实际数组元素的缓冲区，由于一般通过数组的索引获取元素，所以通常不需要使用这个属性
"""
nda_1 = np.arange(20)
print(nda_1)    # [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19]

# 获取nda的秩或者维度
print(nda_1.ndim)  # 1:表示nda是一维数组

# 获取nda的shape
print(nda_1.shape)  # (20,)


nda_2 = np.array([[1,2,3],[4,5,3]])
print(nda_2)
print(nda_2.shape)
