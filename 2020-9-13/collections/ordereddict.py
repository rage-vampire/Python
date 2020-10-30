# -*- coding:utf-8 -*-
# @Filename : ordereddict.py 
# @Author : Lizi
# @Time : 2020/6/17 10:18 
# @Software: PyCharm

from collections import OrderedDict

# 创建有序字典
dic = OrderedDict()
dic['name'] = 'yanglili'
dic['age'] = 24
dic['sex'] = 'women'
print(dic)

# 清空有序字典
dic.clear()
print(dic)

# fromkeys(指定一个列表，把列表中的值作为字典的key,生成一个字典)
dic = OrderedDict()
person = ['name', 'age', 'sex']
dic2 = dic.fromkeys(person)
dic3 = dic.fromkeys(person,'xxx')
print(dic2)
print(dic3)

# move_to_end(指定一个key，把对应的key-value移到最后)
dic = OrderedDict()
dic['name'] = 'yanglili'
dic['age'] = 24
dic['sex'] = 'women'
dic.move_to_end('name')
print(dic)

# pop()获取指定的Key的值，并将该key-value从字典中弹出
k = dic.pop('name')
print(k,dic)

# popitem(按照后进先出原则，删除最后加入的元素，返回key-value，在普通的dic中则是随机弹出一对key_value
dic = OrderedDict()
dic['k1'] = 'v1'
dic['k2'] = 'v2'
dic['k3'] = 'v3'
print(dic.popitem(),dic)
print(dic.popitem(),dic)
