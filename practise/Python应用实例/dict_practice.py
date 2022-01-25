# -*- coding:utf-8 -*-
# @Filename : dict_practice.py 
# @Author : Lizi
# @Time : 2020/3/10 20:43 
# @Software: PyCharm

dic1 = {"k1": "v1", "k2": "v2", "k3": "v3"}
dic2 = {'k1':"v111",'a':"b"}
# 遍历字典 dic1 中所有的key
for k in dic1.keys():
    print(k)
# 遍历字典 dic1 中所有的value
for v in dic1.values():
    print(v)
# 循环遍历字典 dic 中所有的key和value
for k,v in dic1.items():
    print(k,v)

# 添加一个键值对"k4","v4",输出添加后的字典 dic
dic1['k4']='v4'

# 删除字典 dic 中的键值对"k1","v1",并输出删除后的字典 dic
print(dic1.pop("k1"))
# del dic1['k1']

# 删除字典 dic 中 'k5' 对应的值，若不存在，使其不报错，并返回None
print(dic1.pop('k5',None))

# 获取字典 dic 中“k2”对应的值
print(dic1['k2'])

# 获取字典 dic 中“k2”对应的值,若不存在返回None
print(dic1.get('k6'))
dic2.update(dic1)
print(dic1)
print(dic2)


# 10、组合嵌套，实现功能，现有列表如下：
AA = [['k', ['qwe', 20, {'k1': ['tt', 3, '1']}, 89], 'ab']]
# 将列表中的‘tt’变成大写(两种方式)
print(AA[0][1][2].get('k1')[0].upper())
# 将数字 3 变成字符串 ‘100’(两种方式)
AA[0][1][2]['k1'][1]='100'
print(AA)

