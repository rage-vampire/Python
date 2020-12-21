# -*- coding:utf-8 -*-
# @Filename : counter.py 
# @Author : Lizi
# @Time : 2020/6/17 11:01 
# @Software: PyCharm

from collections import Counter

# Counter（计数器）：用于追踪值的出现次数
# Counter类继承dict类，是一个有序集合，其中元素存储为字典的键，计数存储为键的值。所以它能使用dict类里面的方法

# 计算相同的数据出现的次数，以字典形式返回
contries = ['China', 'Albania', "Frank", 'China', 'Albania', "Frank", 'China', "Frank"]
contries_count = Counter(contries)
# print(contries_count)

""" most_common(n)：返回最长见的元素及其个数
    注：如果n为空，则返回所有元素 """
print(f"最常见的元素及其个数：{contries_count.most_common(1)}")



"""elements：返回一个迭代器，其中元素的重复次数与计数次数相同"""
prime_factors = Counter({2: 2, 3: 3, 17: 1})
product = 0
for factor in prime_factors.elements():
    product += factor
print("elements返回值：",list(prime_factors.elements()))
print('相加之后的值为：',product)




# Counter类创建
# c = Counter()
c = Counter('hagnghg')
# c = Counter({'a':1,'b':2})
# c =Counter(a=1, b=2)
print(c)

# c.clear()
print(c.items())
print(c.most_common()[::])


# # 访问的键不存在是，返回0
# print(c['f'])