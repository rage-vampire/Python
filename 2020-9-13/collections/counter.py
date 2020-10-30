# -*- coding:utf-8 -*-
# @Filename : counter.py 
# @Author : Lizi
# @Time : 2020/6/17 11:01 
# @Software: PyCharm

from collections import Counter

# Counter（计数器）：用于追踪值的出现次数
# Counter类继承dict类，所以它能使用dict类里面的方法



# Counter类创建
c = Counter()
c = Counter('hagnghg')
# c = Counter({'a':1,'b':2})
# c =Counter(a=1, b=2)
print(c)

# c.clear()
print(c.items())
print(c.most_common()[::])


# # 访问的键不存在是，返回0
# print(c['f'])