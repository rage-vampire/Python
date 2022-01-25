# -*- coding:utf-8 -*-
# @Filename : nametuple.py 
# @Author : Lizi
# @Time : 2020/6/17 9:53
# @Software: PyCharm

from collections import namedtuple
# 定义一个nametuple类型的Person，包含'name', 'sex', 'age', 'height'属性
Person = namedtuple('person', ['name', 'sex', 'age', 'height'])

# 创建一个lili对象
lili = Person('yanglili', 'women', 24, '170cm')


# 也可以通过一个list来创建一个User对象，这里注意需要使用"_make"方法
# lili = Person._make(['yanglili', 'women', 24, '170cm'])

# 获取对象的值
print(lili)

# 获取用户的属性
print('name:', lili.name)
print('sex:', lili.sex)
print('age:', lili.age)
print('height:', lili.height)

# # 修改对象属性的值，使用_replace
# lili = lili._replace(height='175cm')
# print(lili.height)

#
def get_name():
    Name = namedtuple('name',['first_name','middle_name','last_name'])
    person = Name('aaa','bbb','ccc')
    return person

name = get_name()
print(name.first_name)